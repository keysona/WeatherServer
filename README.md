# WeatherServer
This is a WeatherServer.

# api
根据城市名称来查询天气数据，或者城市id。

为此需要先获得所有城市名与id，由于中国天气网关闭原来的查询接口，所以需要解析下面的xml文件。

必要的城市名与id[在这里](https://gist.githubusercontent.com/keysona/24b77360df35ac211d2be37f93c86932/raw/04eb7a5ef29e6383c50d92e16217c527a63133db/%25E5%259F%258E%25E5%25B8%2582%25E5%2590%258D%25E4%25B8%258Eid.xml)

接口调用形式:

- 城市ID
- 城市名称

    
```

http://www.keysona.com/api/weather/today/countryName/广州

http://www.keysona.com/api/weather/today/countryId/280101

```

# Note
To install scrapy in ubuntu, you should:
```
sudo apt-get install -y libxml2-dev libxslt1-dev libffi-dev
pip install lxml
```
