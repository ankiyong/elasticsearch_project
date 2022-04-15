## cent selenium 오류 발생

cent에서 selenium을 사용하다 보면 오류가 발생한다.





```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(chrome_options=chrome_options)
```

