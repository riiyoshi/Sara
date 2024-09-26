import openai
import discord

# OpenAIのAPIキーをセットアップする
openai.api_key = "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"

# ChatGPTというクラスを定義する
class ChatGPT:
    def __init__(self, system_setting):
        # システムの設定をセットする
        self.system = {"role": "system", "content": system_setting}
        # ユーザーの入力を保持するためのリストを初期化する
        self.input_list = [self.system]
        # ログを保持するためのリストを初期化する
        self.logs = []

    # ユーザーからの入力を受け取り、OpenAI APIを使って回答を生成する
    def input_message(self, input_text):
        # ユーザーの入力をリストに追加する
        self.input_list.append({"role": "user", "content": input_text})
        # OpenAI APIを使って回答を生成する
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.input_list
        )
        # 生成した回答をログに追加する
        self.logs.append(result)
        # 生成した回答をリストに追加する
        self.input_list.append(
            {"role": "assistant", "content": result.choices[0].message.content}
        )

# Discord Botを作成するための準備
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Discord Botが起動したときに呼び出される関数
@client.event
async def on_ready():
    print("起動完了")

# Discordでメッセージが送信されたときに呼び出される関数
@client.event
async def on_message(message):
    # Bot自身が送信したメッセージには反応しない
    if message.author == client.user:
        return

    # ユーザーからの質問を受け取る
    if client.user in message.mentions:
        question = message.content.replace(f'<@{client.user.id}>', '').strip()

        # ChatGPTクラスを使って回答を生成する
        api = ChatGPT(system_setting="あなたはアシスタントです。会話を開始します。")
        api.input_message(question)

        # 生成した回答を取得する
        answer = api.input_list[-1]["content"]

        # 回答を送信する際にユーザーをメンションする
        await message.channel.send(f'<@{message.author.id}> {answer}')

# Discord Botを起動する
client.run("MTI4Nzc2MzA0MTk0OTA1NzAzNA.GKqCps.DkKJd9bim2v4qki4SZX0rgSKRnzkJSfZzG8UA8")
