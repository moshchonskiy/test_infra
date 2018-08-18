import os
import pytest
import requests
import testinfra


@pytest.fixture(scope='module')
def public_ip():
    return os.getenv('PUBLIC_IP', '34.220.232.126')


@pytest.fixture(scope='module')
def public_dns():
    return os.getenv('PUBLIC_DNS', '')


@pytest.fixture(scope='module')
def ssh(public_ip):
    try:
        config_dir = os.getenv('SSH_CONFIG_DIR', '/Users/yevhen/.ssh')
        config = os.path.join(config_dir, 'config')
        connection = testinfra.get_host("ssh://{}".format(public_ip), ssh_config=config)
    except AssertionError:
        return None
    return connection


@pytest.fixture(scope='module')
def nginx(ssh):
    assert ssh, "No ssh connection to the instance!"
    return ssh.package("nginx")


#  Nginx is accessible through external DNS (ELB)
#  Nginx is accessible by ssh using the generated private key
#  Nginx listens at localhost's port 80 at the VM created
#  Nginx config property `worker_processes auto;` is set in service's config
#  Nginx access log is configured correctly and logs incoming HTTP requests with IP address of calling side


def assert_nginx_is_installed(nginx):
    assert nginx.is_installed, 'Nginx is not installed!'


def test_nginx_is_installed(nginx):
    assert_nginx_is_installed(nginx)
    expected_version = "1.15"
    assert nginx.version.startswith(expected_version), 'Installed wrong Nginx version!'


def test_nginx_is_accessible_dns(public_dns):
    assert public_dns, "Public DNS is not provided!"
    resp = requests.get('https://' + public_dns, verify=False, timeout=15)
    assert resp.ok, 'Nginx is not accessible by DNS provided: {}'.format(public_dns)


def test_instance_is_accessible_ssh(ssh):
    assert ssh is not None, "Instance is not accessible by ssh!"


def test_nginx_listens_port(ssh, nginx):
    assert_nginx_is_installed(nginx)
    socket = ssh.socket('tcp://127.0.0.1:80')
    assert socket.is_listening, 'Port is not being listened!'


def test_nginx_proper_config(ssh, nginx):
    assert_nginx_is_installed(nginx)
    config = ssh.file("/etc/nginx/nginx.conf")
    assert config.contains("worker_processes auto;"), 'Nginx config is missing some info!'


def test_nginx_log_is_configured(public_dns, ssh, nginx):
    assert_nginx_is_installed(nginx)
    assert public_dns, "Public DNS is not provided!"
    # TODO: do not use external service
    ip = requests.get('https://api.ipify.org').text
    resp = requests.get('https://' + public_dns, verify=False)
    assert resp.ok
    log = ssh.file("/var/log/hipchat/nginx.log")
    assert log.contains('nginx-access:'), 'Log does not contain nginx-access record!'
    assert log.contains('python-requests'), 'Log does not contain client type record!'
    assert log.contains(ip), 'Log does not contain ip address!'
