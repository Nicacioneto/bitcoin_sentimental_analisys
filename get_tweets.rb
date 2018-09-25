require 'twitter'
require 'json'

client = Twitter::Streaming::Client.new do |config|
  config.consumer_key        = ""
  config.consumer_secret     = ""
  config.access_token        = ""
  config.access_token_secret = ""
end


tweets_stream = File.open("tweets_stream.txt", "a")

topics = ["bitcoin", "btc", "satoshi"]
client.filter(track: topics.join(",")) do |object|
  if object.is_a?(Twitter::Tweet)
    hash = object.to_h
    tweets_stream.write(hash.to_json)
    tweets_stream.write("\n")
  end
end
