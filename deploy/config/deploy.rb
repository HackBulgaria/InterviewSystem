# config valid only for current version of Capistrano
lock '3.4.0'

set :application, 'interview'
set :repo_url, 'https://github.com/HackBulgaria/InterviewSystem.git'

# Default branch is :master
ask :branch, `git rev-parse --abbrev-ref HEAD`.chomp

# Default deploy_to directory is /var/www/my_app_name
set :deploy_to, '/hack/interview'

# Default value for :scm is :git
# set :scm, :git

# Default value for :format is :pretty
# set :format, :pretty

# Default value for :log_level is :debug
# set :log_level, :debug

# Default value for :pty is false
# set :pty, true

# Default value for :linked_files is []
set :linked_files, fetch(:linked_files, []).push('source/interview_communicator/local_settings.py')

# Default value for linked_dirs is []
set :linked_dirs, fetch(:linked_dirs, []).push('static', 'media')

# Default value for default_env is {}
# set :default_env, { path: "/opt/ruby/bin:$PATH" }

# Default value for keep_releases is 5
# set :keep_releases, 5

namespace :deploy do
  task :pip_install do
    on roles(:all) do |h|
      execute "/hack/interview/shared/virtualenv/bin/pip install -r /hack/interview/current/requirements.txt"
    end
  end

  task :run_migrations do
    on roles(:all) do |h|
      execute "/hack/interview/shared/virtualenv/bin/python3 /hack/interview/current/source/manage.py migrate --noinput"
    end
  end

  task :bower_install do
    on roles(:all) do |h|
      execute "cd /hack/interview/current/source/course_interviews/static/ && bower install"
    end
  end

  task :run_collect_static do
    on roles(:all) do |h|
      execute "/hack/interview/shared/virtualenv/bin/python3 /hack/interview/current/source/manage.py collectstatic --noinput"
    end
  end

  task :restart do
    on roles(:all) do |h|
      execute "sudo restart interview"
    end
  end

  after :published, :pip_install
  after :pip_install, :run_migrations
  after :pip_install, :bower_install
  after :bower_install, :run_collect_static
  after :run_migrations, :restart
end