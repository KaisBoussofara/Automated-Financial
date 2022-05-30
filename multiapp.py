"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        auth = st.session_state['authenticator']

        col1, col2, col3 = st.columns([1, 6, 1])
        # app = st.sidebar.radio(
        with st.container():
            with col1 :
               app= st.markdown('Finance Dashboard')
            with col3 :
                app = auth.logout("Logout")
        app = st.selectbox(
            'Navigation',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()