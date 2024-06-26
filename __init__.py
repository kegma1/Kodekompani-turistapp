from flask import Flask
from flask_wtf import CSRFProtect
import secrets
app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024 

app.secret_key = secrets.token_urlsafe(16)

import routes.index
import routes.signup
import routes.login
import routes.logout
import routes.admin
import routes.admin_sights
import routes.admin_sights_edit
import routes.profile
import routes.attractions_list
import routes.attraction_page
import routes.add_attraction
import routes.people_list
import routes.people_page
import routes.unlock_achivement
import routes.following_list
import routes.leaderboard
import routes.get_qr_code

import routes.add_achievement
import routes.admin_achievements_edit
import routes.admin_achievements
import routes.user_achievements
import routes.admin_posts

if __name__ == "__main__":
    app.run()

# user1 = user1pass
# user2 = user2pass
# admin1 = admin1pass
