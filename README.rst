zephyr
#########


Zephyr is a blog cms. it's clone from  `white <https://github.com/whiteclover/white>`_ that a blog cms wrote by flask.
The zephyr project rewrite using Tornado.


Features
================

#. using hocon config and fully console command controll.
#. A flexible autoload-route system and object-oriented domain model architecture
#. writes blog using markdown
#. custom field extension
#. custom theme
#. multi-languages support
#. rss feed
#. simple memozie cache
#. takes advantage of Tornado and Jinjia2


.. image:: https://github.com/whiteclover/white/blob/master/snap/home.png


.. contents::
    :depth: 2

Install
==============


Firstly download or fetch it form github then run the command in shell:

.. code-block:: bash

    pip install -r requirements.txt

or::

Firstly download or fetch it form github then run the command in shell:

.. code-block:: bash

    cd zephyr # the path to the project
    python setup.py install

Development
===========

Fork or download it, then run:

.. code-block:: bash 

    cd zephyr # the path to the project
    python setup.py develop

Compatibility
=============

Built and tested under Python 2.7 

Setup Database
==============

* create database in mysql:
* then run the mysql schema.sql script in the project directoy schema:

.. code-block:: bash

    mysql -u yourusername -p yourpassword yourdatabase < schema.sql


if your database has not been created yet, log into your mysql first using:

.. code-block:: bash

    mysql -u yourusername -p yourpassword yourdatabase
    mysql>CREATE DATABASE a_new_database_name
    # = you can =
    mysql> USE a_new_database_name
    mysql> source mysql.sql



when firstly run the project, please use the root account, then go to user management ui change your account info:

:username: zephyr 
:password: zephyr

Run in console
================



The terminal help options
--------------------------


.. code-block:: bash

	$ python zephyrd -h

	usage: zephyrd [-h] [--asset.url_prefix ASSET.URL_PREFIX]
	               [--asset.path ASSET.PATH] [--db.db DB.DB] [--db.host DB.HOST]
	               [--db.user DB.USER] [--db.passwd DB.PASSWD] [--db.port DB.PORT]
	               [--jinja2.cache_path JINJA2.CACHE_PATH]
	               [--jinja2.cache_size JINJA2.CACHE_SIZE] [--jinja2.auto_reload]
	               [--redis.host REDIS.HOST] [--redis.port REDIS.PORT]
	               [--redis.db REDIS.DB] [--redis.password REDIS.PASSWORD]
	               [--redis.max_connections REDIS.MAX_CONNECTIONS]
	               [-H TORNADO.HOST] [-p TORNADO.PORT] [-d] [--language LANGUAGE]
	               [--theme THEME] [--secert_key SECERT_KEY] [-c FILE]
	               [-v VERSION]

	optional arguments:
	  -h, --help            show this help message and exit

	Asset settings:
	  --asset.url_prefix ASSET.URL_PREFIX
	                        Asset url path prefix: (default '/assets/')
	  --asset.path ASSET.PATH
	                        Asset files path (default
	                        '/code/Zephyr/zephyr/asset')

	DB settings:
	  --db.db DB.DB         The database name (default 'zephyr')
	  --db.host DB.HOST     The host of the database (default 'localhost')
	  --db.user DB.USER     The user of the database (default 'zephyr')
	  --db.passwd DB.PASSWD
	                        The password of the database (default 'zephyr')
	  --db.port DB.PORT     The port of the database (default 3306)

	Jinja2 settings:
	  --jinja2.cache_path JINJA2.CACHE_PATH
	                        Jinja2 cache code byte path: (default None)
	  --jinja2.cache_size JINJA2.CACHE_SIZE
	                        Jinja2 cache size: (default -1)
	  --jinja2.auto_reload  Jinja2 filesystem checks (default False)

	Redis settings:
	  --redis.host REDIS.HOST
	                        The host of the redis (default 'localhost')
	  --redis.port REDIS.PORT
	                        The port of the redis (default 6379)
	  --redis.db REDIS.DB   The db of the redis (default 0)
	  --redis.password REDIS.PASSWORD
	                        The user of the redis (default None)
	  --redis.max_connections REDIS.MAX_CONNECTIONS
	                        The max connections of the redis (default None)

	Service settings:
	  -H TORNADO.HOST, --tornado.host TORNADO.HOST
	                        The host of the tornado server (default 'euterpe')
	  -p TORNADO.PORT, --tornado.port TORNADO.PORT
	                        The port of the tornado server (default 8888)
	  -d, --debug           Open debug mode (default False)
	  --language LANGUAGE   The language for the site (default 'en_GB')
	  --theme THEME         The theme for the site (default 'default')
	  --secert_key SECERT_KEY
	                        The secert key for secure cookies (default
	                        '7oGwHH8NQDKn9hL12Gak9G/MEjZZYk4PsAxqKU4cJoY=')
	  -c FILE, --config FILE
	                        config path (default '/etc/zephyr/app.conf')
	  -v VERSION, --version VERSION
	                        Show zephyr version 0.1.0a


Setup Config file
=====================


Currently, using hocon config. the primary goal of hocon is: keep the semantics (tree structure; set of types; encoding/escaping) from JSON, but make it more convenient as a human-editable config file format.

.. code-block:: python

	# Zehpyr config


	tornado {
		host = "localhost"
		port = 8888
	}

	# theme = "default"
	# languge = "en_GB"

	secert_key = "7oGwHH8NQDKn9hL12Gak9G/MEjZZYk4PsAxqKU4cJoY="

	debug = off

	db {
		passwd = "thomas"
	    user = "root"
	    host = "localhost"
	    db = "zephyr"
	}


	redis {
		host = "localhost"
		port = 6379
	}

	//asset {
	//	url_prefix = "/assets/" // asset url path prefix
	//	path  = "./nodejs/dist/assets" # static files path
	//}


	jinja2 {
		cache_path = "./cache" # mako module cache  path, comments it if wanna  disable 
		auto_reload = on 
	}




Try run
--------------

If you wanna use production mode and ``zephyrd`` running the blog service.

.. code-block:: bash

	> python zephyrd -c=conf/app.conf -d
	[20151101 12:26:06] zephyr[WARNING] autoload - In module zephyr.module.front.model : No module named model
	[20151101 12:26:06] zephyr[WARNING] autoload - In module zephyr.module.menu.model : No module named model
	[20151101 12:26:06] zephyr[WARNING] tornado.application - Multiple handlers named field_page; replacing previous value
	[20151101 12:26:06] zephyr[WARNING] tornado.application - Multiple handlers named post_delete; replacing previous value
	[20151101 12:26:06] zephyr[INFO] app - Starting zephyr on localhost:8888


Run zephyr in Other WSGI Servers
----------------------------------

When you wanna use other wsgi servers, just booststrap app, then take the app in your server api:

.. code-block:: python

	import tornado.wsgi

	from cherrypy.wsgiserver import CherryPyWSGIServer

	from zephyr.app import ZephyrApp
	from zephyr.config import ConfigFactory
	
	if __name__ == "__main__":
		config = ConfigFactory.parseFile('$your_conf', pystyle=True) # or use SelectConfig
		app = ZephyrApp(config)
	    wsgi_app = tornado.wsgi.WSGIAdapter(app)
	    server = CherryPyWSGIServer(
	        (config.get('cherry.host', 'localhost'), config.get('cherry.port', 8888)),
	        wsgi_app,
	        server_name='Zephyr',
	        numthreads=30)
	    try:
	        server.start()
	    except KeyboardInterrupt:
	        server.stop()



LICENSE
=======
Apache License

