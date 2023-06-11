cdmodule.exports = {
  apps : [{
    name: 'users-api',
    script: 'gunicorn',
    args: ['GozleUsers.wsgi', '-c', 'gunicorn_config.py'],
    interpreter: 'python3',
    error_file: '/data/apis/users-error.log',
    out_file: '/data/apis/users-out.log',
    watch: false
  }],
};
