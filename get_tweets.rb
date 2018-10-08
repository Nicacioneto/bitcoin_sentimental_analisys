require 'twitter'
require 'json'
require 'byebug'

client = Twitter::Streaming::Client.new do |config|
  config.consumer_key        = ""
  config.consumer_secret     = ""
  config.access_token        = ""
  config.access_token_secret = ""
end



topics = ["bitcoin", "btc", "satoshi"]
client.filter(track: topics.join(",")) do |object|
  current_day = DateTime.now.day
  file_name = "/home/nicacio_notebook/bitcoin_sentimental_analisys/" + current_day.to_s
  tweets_stream = File.open(file_name, "a")
  if object.is_a?(Twitter::Tweet)
    hash = object.to_h
    tweets_stream.write(hash.to_json)
    tweets_stream.write("\n")
  end
end
