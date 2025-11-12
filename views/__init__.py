# post views
from .post_views import PostsAPI, PostDetailAPI

# comment views
from .comment_views import PostCommentsAPI, CommentDeleteAPI

# auth views
from .auth_views import AuthRegisterView, AuthLoginView

# category views
from .category_views import CategoriesAPI, CategoryDetailAPI

# user views
from .user_views import UsersAPI, UserDetailAPI, UserRolePatchAPI

# stats views
from .stats_views import StatsAPI