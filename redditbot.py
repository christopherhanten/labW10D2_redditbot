
import praw, time, csv, random, itertools, requests
#name the bot
BOT = 'spirit_of_mckenna'
#get pw from user
PASSWORD = "" #not actual password
#verify password
KEYWORD = "mckenna"
#render about of time app's been asleep
SLEEP_MESSAGE = "Sleeping for 12 hours..."
#Who built this dang ole thing?
BY_LINE = " -Terence McKenna"
# not sure
USER_AGENT = "When people reference McKenna, I provide a quote of his, /u/spirit_of_mckenna"
#what /r's am I looking in?
SUBREDDITS = [ 'test',
              'psychonaut',
              'rationalpsychonaut',
              'conspiro',
              'joerogan',
              'heavymind',
              'woahdude',
              'news',
              'worldnews',
              'quotesporn',
              'shamanism',
              'luciddreaming',
              'interestingasfuck',
              'holofractal',
              'futurology',
              'futureporn',
              'learnprogramming'
              ]
#create the Bot
class Bot:
#instantiate the app
    def __init__(self):
        # Let user know that the bot is firing up
        print("Initializing Bot")
        self.quotes = []
        self.cache = []
        self.logged_in = False
        self.r = praw.Reddit(user_agent = USER_AGENT)

        self.parse_quotes()
        self.parse_cache()
        self.log_in()
        while True:
          self.run()
#from here down, I am lost!
    def run(self):
          try:
              self.get_subs()
          except praw.errors.RateLimitExceeded as error:
              print('\tSleeping for %d seconds' % error.sleep_time)
              time.sleep(error.sleep_time)
          except requests.exceptions.ConnectionError as error:
              self.wait(error)
          except KeyboardInterrupt:
              raise
          except:
              self.wait('')

          self.save_cache()
          self.wait("All Subreddits checked.")

    def parse_quotes(self):
        with open('quotes.csv') as csvfile:
            for row in csvfile:
                self.quotes.append(row.decode('utf-8'))

    def parse_cache(self):
        f = open('cache.csv')
        for row in csv.reader(f):
            self.cache.append(row)
        from itertools import chain
        chain = itertools.chain.from_iterable(self.cache)
        self.cache = list(chain)

    def wait(self, tag):
      print tag
      print SLEEP_MESSAGE
      time.sleep(43200)

    def log_in(self):
        while not self.logged_in:
            try:
              self.r.login(BOT, PASSWORD)
              self.logged_in = True
              print("logging in...")
            except requests.exceptions.ConnectionError:
                tag = 'No web connection.'
                self.wait(tag)

    def get_subs(self):
        for subreddit in SUBREDDITS:
            sub = self.r.get_subreddit(subreddit)
            print("getting subreddit " + str(subreddit.title()))
            self.get_comments_for_sub(sub)

    def get_comments_for_sub(self, sub):
        comments = sub.get_comments(limit=199)
        print("getting comments...")
        for comment in comments:
            comment_text = comment.body.lower()
            if self.has_keyword(comment_text) and self.not_bot(comment) and self.not_in_cache(comment):
                self.reply_to_comment(sub, comment)

    def has_keyword(self, comment_text):
        if KEYWORD in comment_text:
            return True

    def not_bot(self, comment):
        if comment.author and comment.author.name != BOT:
            return True

    def not_in_cache(self, comment):
        if comment.id not in self.cache:
            return True

    def reply_to_comment(self, sub, comment):
        quote = random.choice(self.quotes)
        if len(quote) > 1:
            comment.reply(quote[:-2] + BY_LINE)
            print("replying to comment in " + sub.title + " with " + quote[:-2])
            self.cache.append(comment.id)
            self.save_cache()

    def save_cache(self):
        myfile = open('cache.csv', 'wb')
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(self.cache)


if __name__ == '__main__':
  mckenna = Bot()
