from db_utils import db_session, UserPosts, Attraction
from libs.helpers import get_curr_user

def create_post(attraction_id = None, message = "", image_data = None, is_status = False):
   new_post = UserPosts(message, get_curr_user().id, attraction_id, is_status)

   print(image_data)

   if image_data:
      new_post.image = image_data.stream

   db_session.add(new_post)
   db_session.commit()