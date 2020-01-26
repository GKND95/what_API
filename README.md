## Backend Python API for 'What' Chrome extension

#### Concordia University Hacks 2020

#### Team: Yaniv Silberman, Olga Sanchis, Gavin Dove, Kees Vandenberg

#### Authored by: Gavin Dove, January 2020 <br/> <br/>


See repo for 'What' front end code at: https://github.com/YanivSilberman/what-client <br/> <br/>

Set-up: <br/>

Note: Requires ngrok to be running on same port as gunicorn   https://ngrok.com/

1. Activate virtual environment inside outer what_API folder

2. Add environment variable for path to google translate API key: <br/>
    $ export GOOGLE_APPLICATION_CREDENTIALS="path/to/key"
    
3. Add environment variable for path to nltk dataset <br/>
    $ export NLTK_DATA="path/to/nltk_data"
    
4. Start gunicorn: <br/>
    $ gunicorn --reload what_API.app
    
5. Activate ngrok on same port as gunicorn <br/> <br/>

API routes:

/sentence:        logic for selecting and translating random sentences on web page

/word_lookup:     logic for translating highlighted english or french words on web page

/word:            logic for translating individual words according to user selected word-type, frequency & difficulty
