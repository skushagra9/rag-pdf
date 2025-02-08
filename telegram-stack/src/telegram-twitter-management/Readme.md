# 🚀 Telegram Twitter Management Bot

A **Telegram bot** that allows users to **draft, edit, approve, and post tweets** directly from a Telegram chat. The bot integrates with the **Twitter API v2** to publish tweets and provides an interactive interface using **inline keyboards**.

## ✨ Features

- **Draft Tweets** – Users can create tweet drafts from Telegram.
- **List Pending Tweets** – View all pending tweets in an interactive list.
- **Approve & Post** – Easily approve and publish a tweet to Twitter.
- **Edit Tweets** – Modify a pending tweet before posting.

## Demo Video



## Commands & Usage

### 1.Start the Bot
```sh
/start
```
#### Response:
```sh
Hello! Use /tweet <idea> to begin drafting a tweet.
```
### 2. Create a Tweet Draft

```sh
/tweet This is my new tweet!
```

#### Response:
```sh
Proposed Tweet Draft:

This is my new tweet!

Use /approve to post, or /edit <text> to modify.

List Pending Tweets
```
### 3. /list

#### Response:
```sh
Select a Tweet to Manage:
[ Tweet preview ]

Approve & Post a Tweet

Click the Approve & Post button from the inline menu.
```
```sh
Response (if successful):

Tweet posted successfully!
View Tweet: https://twitter.com/i/web/status/<tweet_id>
```
```sh
Response (if failed):

Failed to post tweet.

Edit a Draft

Click the Edit button in the inline menu.
```
```sh
Response:

Send the new text for tweet ID <tweet_id>:

Then, send the new tweet text.
```
```sh
Response after editing:

Tweet updated:
ID <tweet_id>
New Text: <updated_text>

```