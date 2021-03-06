# Integrate Communication Channels into Your Python App

## âšī¸ Prerequisites
- Basic Python knowledge 
- Python 3.6+ <br>
- Installed [virtual env](https://pypi.org/project/virtualenv/)

## â Checks
First you need to know what version of python are you using:

```bash     
python --version
```
```bash
which python  
```
```bash
which pip
```

## đĄ  Agenda
Enable app to use various communication channels such as:
- [SMS Reference](https://www.infobip.com/docs/api#channels/sms)
- [Whatsapp Reference](https://www.infobip.com/docs/api#channels/whatsapp)
- [Email Reference](https://www.infobip.com/docs/api#channels/email)

## đ Jump start
### Install packages
```bash
pip install -r requirements/dev.txt
```
### Run the app
```bash
uvicorn main:app --reload
```
### Localhost address
- http://localhost:8000
