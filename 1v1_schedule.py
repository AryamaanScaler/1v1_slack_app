from http.server import BaseHTTPRequestHandler
from utils import post_message
from slack import WebClient
 
class handler(BaseHTTPRequestHandler):
 
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()

    slack_client = WebClient(os.environ.get('SLACK_BOT_TOKEN'))
    post_message(slack_client, "U04U41MRT8S", "hello")
    return