#!/usr/bin/env python3
# coding=utf-8

from flask import render_template, render_template_string, flash, redirect, session, url_for, request, g, Markup, Response, abort
from app import app

import requests
import logging
import uuid
import json
import re
import urllib
import urlparse
import socket


REQUEST_SETTINGS = {
    'allow_redirects': True,
    'verify': False,
    'timeout': 3
}


RANK_LOW, RANK_MEDIUM, RANK_HIGH = 'low', 'medium', 'high'
WEBSITE_RANKING = {
    'ohio state university': RANK_LOW,
    'osu.edu': RANK_LOW,
    'oklahoma state university': RANK_LOW,
    'okstate.edu': RANK_LOW,
    'debian.org': RANK_MEDIUM,
    'oregon state university': RANK_HIGH,
    'oregonstate.edu': RANK_HIGH,
    'archlinux.org': RANK_HIGH
}


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/api/rank')
def api_rank():
    # external only API
    if request.remote_addr == '127.0.0.1':
        return abort(401)

    url = request.args.get('url')
    if not url:
        return Response(response=json.dumps({'success': False, 'url': url, 'rank': None, 'message': 'Parameter `url` required'}), status=400, mimetype='application/json')

    try:
        # try to resolve the domain in case they configure DNS to make a 
        # domain point to a private IP
        if _is_private_ip(socket.gethostbyname_ex(urlparse.urlparse(url).netloc)[2][0]):
            return Response(response=json.dumps({'success': False, 'url': url, 'rank': None, 'message': 'We don\'t allow SSRF here! Private IP addresses are not allowed'}), status=400, mimetype='application/json')
    except socket.gaierror:
        return Response(response=json.dumps({'success': False, 'url': url, 'rank': None, 'message': 'Cannot resolve domain'}), status=400, mimetype='application/json')
    

    content = requests.get(url, **REQUEST_SETTINGS).text.lower()
    
    for c, r in WEBSITE_RANKING.items():
        if c.lower() in content:
            rank = r
            break
    else:
        rank = RANK_MEDIUM

    # TODO store in database
    return Response(response=json.dumps({'success': True, 'url': url, 'rank': rank, 'message': 'Ranked webpage'}), status=200, mimetype='application/json')


@app.route('/api/status')
def api_status():
    # external only API
    if request.remote_addr == '127.0.0.1':
        return abort(401)

    host = request.host
    ssh_port = 22 #forwarded port is 31322
    http_port = 8180 #forwarded port is 31321

    response = {
        'ssh': {
            'port': ssh_port,
            'online': "requests.exceptions.ConnectionError: ('Connection aborted.', BadStatusLine('SSH-" in requests.get('http://127.0.0.1:8180/api/_internal/log-request?port=' + str(ssh_port), **REQUEST_SETTINGS).json()['log']
        },

        'http': {
            'port': http_port,
            'online': requests.get('http://127.0.0.1:8180/api/_internal/log-request?port=' + str(http_port) + '&path=/', **REQUEST_SETTINGS).json()['code'] == 200
        }
    }

    return Response(response=json.dumps(response), status=200, mimetype='application/json')


##########
# Internal API
# TODO move to another host
##########


@app.route('/api/_internal/log-request')
def api_internal_make_request():
    # internal only API
    if request.remote_addr != '127.0.0.1':
        return abort(401)

    # setup logging
    _logger_name = 'make-request-' + str(uuid.uuid4())
    _logger_filename = request.args.get('debug') or '/tmp/%s' % _logger_name
    logger = logging.getLogger(_logger_name)
    logger.setLevel(logging.DEBUG)
    _lfh = logging.FileHandler(_logger_filename, mode='w')
    _lfh.setLevel(logging.DEBUG)
    logger.addHandler(_lfh)

    # gather http req details
    http_method = request.args.get('method', 'GET')
    http_port = int(request.args.get('port', 0))
    http_url_path = request.args.get('path', '/')
    http_url_args = request.args.get('args')
    dest_url = 'http://127.0.0.1' + (':' + str(http_port) if http_port else '') + http_url_path + ('?' + http_url_args if http_url_args else '')

    # make the http request
    success = False
    status_code = None
    try:
        logger.info('Making HTTP request to URL')
        r = requests.request(http_method, dest_url, **REQUEST_SETTINGS)
        logger.info('Read %d bytes from URL (code %d)' % (len(r.text), r.status_code))

        success = True
        status_code = r.status_code
    except:
        logger.exception('Failed to make HTTP request to URL')
    
    # return response
    with open(_logger_filename, 'r') as f:
        return Response(response=json.dumps({
            'success': success,
            'code': status_code,

            'http': {
                'method': http_method,
                'url': dest_url,
                'url_host': '127.0.0.1',
                'url_path': http_url_path,
                'url_args': http_url_args
            },

            'log_filename': _logger_filename,
            'log': f.read()
        }), status=200, mimetype='application/json')


# https://stackoverflow.com/a/28532296/3678023
def _is_private_ip(ip):
    priv_lo = re.compile("^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    priv_24 = re.compile("^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    priv_20 = re.compile("^192\.168\.\d{1,3}.\d{1,3}$")
    priv_16 = re.compile("^172.(1[6-9]|2[0-9]|3[0-1]).[0-9]{1,3}.[0-9]{1,3}$")
    return any([priv_lo.match(ip), priv_24.match(ip), priv_20.match(ip), priv_16.match(ip)])
