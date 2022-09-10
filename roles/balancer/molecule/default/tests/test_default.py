import os
import pytest
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_service_running_and_enabled(host,):
    if host.file('/etc/redhat-release').exists:
        service = host.service('haproxy')
        assert service.is_running
        assert service.is_enabled
    else:
        # BUG: testinfra tries to use systemd
        out = host.check_output('service haproxy status')
        assert out == 'haproxy is running.'


@pytest.mark.parametrize('name', [
    'haproxy.log',
    'haproxy-http.log',
    'haproxy-tcp.log',
])
def test_logfiles(host, name):
    with host.sudo():
        assert host.file('/var/log/haproxy/%s' % name).exists


@pytest.mark.parametrize('command', [
    "curl -s http://localhost/",
    "curl -ks https://localhost:443/"])
def test_http(host, command):
    out = host.check_output(command)
    assert '503 Service Unavailable' in out
    assert 'No server is available to handle this request.' in out
    with host.sudo():
        log = host.file('/var/log/haproxy/haproxy-http.log')
        lastline = log.content_string.splitlines()[-1]
        assert re.match(r'.*[01]/[01]/0/0/0 0/0 "GET / HTTP/1.1"', lastline)


def test_tcp(host):
    out = host.check_output("curl -s http://localhost:81/")
    assert '503 Service Unavailable' in out
    assert 'No server is available to handle this request.' in out
    with host.sudo():
        log = host.file('/var/log/haproxy/haproxy-tcp.log')
        assert log.content_string.splitlines()[-1].endswith(
            '/0/0/0 0/0')
