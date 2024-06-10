@app.route('/user')
def user():
    if 'loggedin' in session and session['loggedin']:
        return render_template('user.html', name=session.get('name'))
    else:
        return redirect(url_for('login'))
