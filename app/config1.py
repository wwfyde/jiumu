from pathlib import Path

import yaml
from yaml import FullLoader

from app import log






#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""
配置分类：
1. Django使用的配置文件，写到settings中
2. 程序需要, 用户不需要更改的写到settings中
3. 程序需要, 用户需要更改的写到本config中
"""
import os
import re
import sys
import types
import errno
import json
import yaml
from importlib import import_module
# from django.urls import reverse_lazy
# from django.templatetags.static import static
from urllib.parse import urljoin, urlparse
# from django.utils.translation import ugettext_lazy as _

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# PROJECT_DIR = os.path.dirname(BASE_DIR)

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

# with open(BASE_DIR.joinpath('etc', 'config.yml')) as f:
#     config: dict = yaml.load(f, Loader=FullLoader)
#     # print(config)
#     pass


def import_string(dotted_path):
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        ) from err


class Config(dict):
    """Works exactly like a dict but provides ways to fill it from files
    or special dictionaries.  There are two common patterns to populate the
    config.

    Either you can fill the config from a config file::

        app.config.from_pyfile('yourconfig.cfg')

    Or alternatively you can define the configuration options in the
    module that calls :meth:`from_object` or provide an import path to
    a module that should be loaded.  It is also possible to tell it to
    use the same module and with that provide the configuration values
    just before the call::

        DEBUG = True
        SECRET_KEY = 'development key'
        app.config.from_object(__name__)

    In both cases (loading from any Python file or loading from modules),
    only uppercase keys are added to the config.  This makes it possible to use
    lowercase values in the config file for temporary values that are not added
    to the config or to define the config keys in the same file that implements
    the application.

    Probably the most interesting way to load configurations is from an
    environment variable pointing to a file::

        app.config.from_envvar('YOURAPPLICATION_SETTINGS')

    In this case before launching the application you have to set this
    environment variable to the file you want to use.  On Linux and OS X
    use the export statement::

        export YOURAPPLICATION_SETTINGS='/path/to/config/file'

    On windows use `set` instead.

    :param root_path: path to which files are read relative from.  When the
                      config object is created by the application, this is
                      the application's :attr:`~flask.Flask.root_path`.
    :param defaults: an optional dictionary of default values
    """
    defaults = {
        # Django Config, Must set before start
        'SECRET_KEY': '123',
        'BOOTSTRAP_TOKEN': '',
        'DEBUG': False,
        'LOG_LEVEL': 'DEBUG',
        'LOG_DIR': os.path.join(PROJECT_DIR, 'logs'),
        'DB_ENGINE': 'mysql',
        'DB_NAME': 'jumpserver',
        'DB_HOST': '127.0.0.1',
        'DB_PORT': 3306,
        'DB_USER': 'root',
        'DB_PASSWORD': '',
        'REDIS_HOST': '127.0.0.1',
        'REDIS_PORT': 6379,
        'REDIS_PASSWORD': '',
        # Default value
        'REDIS_DB_CELERY': 3,
        'REDIS_DB_CACHE': 4,
        'REDIS_DB_SESSION': 5,
        'REDIS_DB_WS': 6,

        'GLOBAL_ORG_DISPLAY_NAME': '',
        'SITE_URL': 'http://localhost:8080',
        'CAPTCHA_TEST_MODE': None,
        'TOKEN_EXPIRATION': 3600 * 24,
        'DISPLAY_PER_PAGE': 25,
        'DEFAULT_EXPIRED_YEARS': 70,
        'SESSION_COOKIE_DOMAIN': None,
        'CSRF_COOKIE_DOMAIN': None,
        'SESSION_COOKIE_AGE': 3600 * 24,
        'SESSION_EXPIRE_AT_BROWSER_CLOSE': False,
        # 'LOGIN_URL': reverse_lazy('authentication:login'),

        # Custom Config
        # Auth LDAP settings
        'AUTH_LDAP': False,
        'AUTH_LDAP_SERVER_URI': 'ldap://localhost:389',
        'AUTH_LDAP_BIND_DN': 'cn=admin,dc=jumpserver,dc=org',
        'AUTH_LDAP_BIND_PASSWORD': '',
        'AUTH_LDAP_SEARCH_OU': 'ou=tech,dc=jumpserver,dc=org',
        'AUTH_LDAP_SEARCH_FILTER': '(cn=%(user)s)',
        'AUTH_LDAP_START_TLS': False,
        'AUTH_LDAP_USER_ATTR_MAP': {"username": "cn", "name": "sn", "email": "mail"},
        'AUTH_LDAP_CONNECT_TIMEOUT': 10,
        'AUTH_LDAP_SEARCH_PAGED_SIZE': 1000,
        'AUTH_LDAP_SYNC_IS_PERIODIC': False,
        'AUTH_LDAP_SYNC_INTERVAL': None,
        'AUTH_LDAP_SYNC_CRONTAB': None,
        'AUTH_LDAP_USER_LOGIN_ONLY_IN_USERS': False,
        'AUTH_LDAP_OPTIONS_OPT_REFERRALS': -1,






    }

    def compatible_auth_openid_of_key(self):
        """
        兼容OpenID旧配置 (即 version <= 1.5.8)
        因为旧配置只支持OpenID协议的Keycloak实现,
        所以只需要根据旧配置和Keycloak的Endpoint说明文档，
        构造出新配置中标准OpenID协议中所需的Endpoint即可
        (Keycloak说明文档参考: https://www.keycloak.org/docs/latest/securing_apps/)
        """
        if not self.AUTH_OPENID:
            return

        realm_name = self.AUTH_OPENID_REALM_NAME
        if realm_name is None:
            return

        compatible_keycloak_config = [
            (
                'AUTH_OPENID_PROVIDER_ENDPOINT',
                self.AUTH_OPENID_SERVER_URL
            ),
            (
                'AUTH_OPENID_PROVIDER_AUTHORIZATION_ENDPOINT',
                '/realms/{}/protocol/openid-connect/auth'.format(realm_name)
            ),
            (
                'AUTH_OPENID_PROVIDER_TOKEN_ENDPOINT',
                '/realms/{}/protocol/openid-connect/token'.format(realm_name)
            ),
            (
                'AUTH_OPENID_PROVIDER_JWKS_ENDPOINT',
                '/realms/{}/protocol/openid-connect/certs'.format(realm_name)
            ),
            (
                'AUTH_OPENID_PROVIDER_USERINFO_ENDPOINT',
                '/realms/{}/protocol/openid-connect/userinfo'.format(realm_name)
            ),
            (
                'AUTH_OPENID_PROVIDER_END_SESSION_ENDPOINT',
                '/realms/{}/protocol/openid-connect/logout'.format(realm_name)
            )
        ]
        for key, value in compatible_keycloak_config:
            self[key] = value


    def compatible(self):
        """
        对配置做兼容处理
        1. 对`key`的兼容 (例如：版本升级)
        2. 对`value`做兼容 (例如：True、true、1 => True)

        处理顺序要保持先对key做处理, 再对value做处理,
        因为处理value的时候，只根据最新版本支持的key进行
        """
        parts = ['key', 'value']
        targets = ['auth_openid']
        for part in parts:
            for target in targets:
                method_name = 'compatible_{}_of_{}'.format(target, part)
                method = getattr(self, method_name, None)
                if method is not None:
                    method()

    def convert_type(self, k, v):
        default_value = self.defaults.get(k)
        if default_value is None:
            return v
        tp = type(default_value)
        # 对bool特殊处理
        if tp is bool and isinstance(v, str):
            if v.lower() in ("true", "1"):
                return True
            else:
                return False
        if tp in [list, dict] and isinstance(v, str):
            try:
                v = json.loads(v)
                return v
            except json.JSONDecodeError:
                return v

        try:
            if tp in [list, dict]:
                v = json.loads(v)
            else:
                v = tp(v)
        except Exception:
            pass
        return v

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))

    def get_from_config(self, item):
        try:
            value = super().__getitem__(item)
        except KeyError:
            value = None
        return value

    def get_from_env(self, item):
        value = os.environ.get(item, None)
        if value is not None:
            value = self.convert_type(item, value)
        return value

    def get(self, item):
        # 再从配置文件中获取
        value = self.get_from_config(item)
        if value is not None:
            return value
        # 其次从环境变量来
        value = self.get_from_env(item)
        if value is not None:
            return value
        return self.defaults.get(item)

    def __getitem__(self, item):
        return self.get(item)

    def __getattr__(self, item):
        return self.get(item)


class ConfigManager:
    config_class = Config

    def __init__(self, root_path=None):
        self.root_path = root_path
        self.config = self.config_class()

    def from_pyfile(self, filename, silent=False):
        """Updates the values in the config from a Python file.  This function
        behaves as if the file was imported as module with the
        :meth:`from_object` function.

        :param filename: the filename of the config.  This can either be an
                         absolute filename or a filename relative to the
                         root path.
        :param silent: set to ``True`` if you want silent failure for missing
                       files.

        .. versionadded:: 0.7
           `silent` parameter.
        """
        if self.root_path:
            filename = os.path.join(self.root_path, filename)
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename, mode='rb') as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True

    def from_object(self, obj):
        """Updates the values from the given object.  An object can be of one
        of the following two types:

        -   a string: in this case the object with that name will be imported
        -   an actual object reference: that object is used directly

        Objects are usually either modules or classes. :meth:`from_object`
        loads only the uppercase attributes of the module/class. A ``dict``
        object will not work with :meth:`from_object` because the keys of a
        ``dict`` are not attributes of the ``dict`` class.

        Example of module-based configuration::

            app.config.from_object('yourapplication.default_config')
            from yourapplication import default_config
            app.config.from_object(default_config)

        You should not use this function to load the actual configuration but
        rather configuration defaults.  The actual config should be loaded
        with :meth:`from_pyfile` and ideally from a location not within the
        package because the package might be installed system wide.

        See :ref:`config-dev-prod` for an example of class-based configuration
        using :meth:`from_object`.

        :param obj: an import name or object
        """
        if isinstance(obj, str):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self.config[key] = getattr(obj, key)

    def from_json(self, filename, silent=False):
        """Updates the values in the config from a JSON file. This function
        behaves as if the JSON object was a dictionary and passed to the
        :meth:`from_mapping` function.

        :param filename: the filename of the JSON file.  This can either be an
                         absolute filename or a filename relative to the
                         root path.
        :param silent: set to ``True`` if you want silent failure for missing
                       files.

        .. versionadded:: 0.11
        """
        if self.root_path:
            filename = os.path.join(self.root_path, filename)
        try:
            with open(filename) as json_file:
                obj = json.loads(json_file.read())
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        return self.from_mapping(obj)

    def from_yaml(self, filename, silent=False):
        if self.root_path:
            filename = os.path.join(self.root_path, filename)
        try:
            with open(filename, 'rt', encoding='utf8') as f:
                obj = yaml.load(f, Loader=FullLoader)
                # print(obj)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        if obj:
            return self.from_mapping(obj)
        return True

    def from_mapping(self, *mapping, **kwargs):
        """Updates the config like :meth:`update` ignoring items with non-upper
        keys.

        .. versionadded:: 0.11
        """
        mappings = []
        if len(mapping) == 1:
            if hasattr(mapping[0], 'items'):
                mappings.append(mapping[0].items())
            else:
                mappings.append(mapping[0])
        elif len(mapping) > 1:
            raise TypeError(
                'expected at most 1 positional argument, got %d' % len(mapping)
            )
        mappings.append(kwargs.items())
        for mapping in mappings:
            for (key, value) in mapping:
                if key.isupper():
                    self.config[key] = value
        return True

    def load_from_object(self):
        sys.path.insert(0, PROJECT_DIR)
        try:
            from config1 import config as c
            self.from_object(c)
            return True
        except ImportError:
            pass
        return False

    def load_from_yml(self):
        for i in ['config.yml', 'config.yaml']:
            if not os.path.isfile(os.path.join(self.root_path, i)):
                continue
            loaded = self.from_yaml(i)
            if loaded:
                return True
        return False

    @classmethod
    def load_user_config(cls, root_path=None, config_class=None):
        config_class = config_class or Config
        cls.config_class = config_class
        if not root_path:
            root_path = BASE_DIR

        manager = cls(root_path=root_path)
        if manager.load_from_object():
            config = manager.config
        elif manager.load_from_yml():
            config = manager.config
        else:
            msg = """

            Error: No config file found.

            You can run `cp config_example.yml config.yml`, and edit it.
            """
            raise ImportError(msg)

        # 对config进行兼容处理
        config.compatible()
        return config


if __name__ == '__main__':
    demo = Config()
    print(BASE_DIR)
    config = ConfigManager.load_user_config(root_path=os.path.join(BASE_DIR, 'etc'))
    print(config.get('yunwen'), os.path.join(BASE_DIR, 'etc'))
    print(demo.SECRET_KEY)
    log.info('print')
    log.error("错误")
    pass
