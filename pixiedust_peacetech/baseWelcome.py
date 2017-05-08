from pixiedust.display.app import *
from pixiedust.utils import Logger, cache
from pixiedust.utils.shellAccess import ShellAccess
from datetime import datetime, timedelta
import requests
from pandas.io.json import json_normalize
import pandas
import json

baseUrl = "https://j26ovra6z7.execute-api.us-east-1.amazonaws.com/prod/"
indicators = ["Economy", "Energy", "Law & Order", "Environment", "Labor"]

@PixieApp
@Logger()
class BaseWelcome():
    indicators = ["Food", "Environment", "Civil Unrest", "Infrastructure", "Crime"]

    # @cache(fieldName="_alerts")
    def getAlerts(self, location=None):
        startDate = self.startDate.strftime("%Y%m%d")
        endDate = self.endDate.strftime("%Y%m%d")
        if location is not None and endDate is not None:
            restUrl = "{0}alerts/search?startDate={1}&endDate={2}&location={3}".format(baseUrl, startDate, endDate, location)
            return self.normalize(requests.get(restUrl, headers=ShellAccess.headers).json())
        else:
            return self.normalize(requests.get(baseUrl+"alerts?eventDate="+startDate, headers=headers).json())

    def normalize(self, jsonPayload):
        if len(jsonPayload) > 0:
            return json_normalize(jsonPayload)
        return pandas.DataFrame()
    
    def getAlert(self, alertKey):
        resp = requests.get(baseUrl+"alerts/"+alertKey, headers=ShellAccess.headers).json()
        return self.normalize(resp)
    
    def getNews(self):
        startDate = self.startDate.strftime("%Y%m%d")
        endDate = self.endDate.strftime("%Y%m%d")
        woeid = self.selectedCountry
        restUrl = "{0}demo/news?startDate={1}&endDate={2}&woeid={3}".format(baseUrl, startDate, endDate, woeid)
        return self.normalize(requests.get(restUrl, headers=ShellAccess.headers).json())

    def getMappedAlerts(self):
        startDate = self.startDate.strftime("%Y%m%d")
        endDate = self.endDate.strftime("%Y%m%d")
        woeid = self.selectedCountry
        restUrl = "{0}demo/alerts?startDate={1}&endDate={2}&location={3}".format(baseUrl, startDate, endDate, woeid)
        return self.normalize(requests.get(restUrl, headers=ShellAccess.headers).json())        

    #subclass can override
    def onCountrySelected(self):
        pass
    
    @route()
    def baseWelcome(self, landingPage="baseWelcome.html", **kwargs):
        if ShellAccess.headers is None:
            return "<div>Error, you must define the GroudTruth DataHub credentials in a variable called headers</div>"

        self.endDate = datetime.today()
        self.startDate = self.endDate - timedelta(days=14)
        self._addHTMLTemplate(landingPage, **kwargs)