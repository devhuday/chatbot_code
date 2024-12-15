import queueUser as queue

def user():
  message = queue.Queue()
  if message.verify_queue():
    message.send_message()