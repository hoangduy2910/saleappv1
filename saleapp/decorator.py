from flask import request, redirect, url_for, session
from functools import wraps


def login_required(f):
  @wraps(f)
  def check(*args, **kwargs):
    if not session.get("user"):
      return redirect(url_for("login", next=request.url))

    return f(*args, **kwargs)

  return check