require 'daemons'

options = {
  :app_name   => "get_tweets",
  :backtrace  => true,
  :monitor    => true,
}

Daemons.run('get_tweets.rb', options)
