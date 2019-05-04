![ScrapyLogo](logos/scrapy-logo.png)
# Scrapy – The complete web scraping framework

For those of you who are familiar with Django, Scrapy is a lot similar to it.<br>
The requests we make on Scrapy are scheduled and processed asynchronously, this happens because it is built on top of Twisted, an asynchronous framework.<br>

## Pros
* Good Documentation
* CPU usage is a lot lesser
* Consumes lesser memory
* Extremely efficient in comparison
* The well-designed architecture offers you both robustness and flexibility.
* You can easily develop custom middle-ware or pipeline to add custom functionalities

## Cons
* Overkill for simple jobs
* Might be difficult to install.
* The learning curve is quite steep.
* Not very beginner-friendly, since it is a full-fledged framework

## Best Use Case
* Scrapy is best if you need to build a real spider or web-crawler for large web scraping needs, instead of just scraping a few pages here and there. It can offer extensibility and flexibility to your project. 

![RequestsLogo](logos/requests-logo.png)
# Requests – HTTP for humans

Requests is the perfect example how beautiful an API can be with the right level of abstraction.

## Pros
* Thread-safe.
* Good Documentation
* Multipart File Uploads & Connection Timeouts
* Elegant Key/Value Cookies & Sessions with Cookie Persistence
* Automatic Decompression
* Basic/Digest Authentication
* Browser-style SSL Verification
* Keep-Alive & Connection Pooling
* No need to manually add query strings to your URLs
* Supports the entire restful API, i.e., all its methods – PUT, GET, DELETE, POST.

## Cons
* If your web page has javascript hiding or loading content, then requests might not be the way to go.

## Best Use Case
* If you are a beginner, and your scraping task is simple and contains no javascript elements

![SeleniumLogo](logos/selenium-logo.png)
# Selenium – The automator
Selenium is a tool automates browsers based on Java. Though primarily used as a tool for writing automated tests for web applications, it has come to some heavy use for pages that have javascript on them.

## Pros
* Beginner friendly
* You get real browser to see whats going on (unless you are on a headless mode )
* Mimics human behavior while browsing, including clicks, selection, filling text box, scroll etc.
* Renders a full webpage and shows HTML rendered via XHR or Javascript

## Cons
* Very slow
* Heavy memory use
* High CPU usage.

## Best Use Case
* When you need to scrape sites with data tucked away by JavaScript.
