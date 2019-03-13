from flask import render_template

def register(blueprint):
    """Register the routes for the root app"""
    @blueprint.route('/')
    def index():
        """Main page for the phone calls blueprint"""
        return render_template('index.html')