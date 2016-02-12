Cauthon
=======

Cauthon is a web crawler and processing engine, with filters based on the
Salt loader system.

.. code-block:: python

    import cauthon
    crawler = cauthon.Crawler()
    links = crawler.scrape('http://example.com/path/to/page.html')

TO DO
-----
* Change sqlite schema to map from URL to checksum to content, using some sort
  of hashmap.
* Allow Cauthon to connect to other workers and command them.
* Splay processing and downloading across multiple workers.
* Add more intelligent methods for running filters than just a site map. Filters
  which analyze pages to categorize and rank them cannot be constrained to use
  filters based on domain name.
* Support other databases than sqlite.
 * Genesis should be added as a generic database driver.

Spoiler Alert
-------------
Cauthon is named after Mat Cauthon, from Robert Jordan's The Wheel of Time
series. Towards the beginning of the series Mat finds himself with holes in his
memory. Later he meets two races, the Aelfinn and the Eelfinn, who grant him
the answers to three questions, and later three wishes, one of which fills the
holes in his memory with memories collected from dead soldiers, and military
leaders. With these memories Mat unwillingly becomes a great general, eventually
commanding a number of armies.

The Cauthon web crawler is so named in part because it can collect data from
various sources, and compile it into a larger database. It can analyze those
data to reach certain conclusions. It also has the ability to command other
instances of itself, increasing its ability to complete the task at hand.
