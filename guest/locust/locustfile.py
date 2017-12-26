#!/usr/bin/env python3
#-*- coding:utf-8 -*-
from locust import HttpLocust, TaskSet, task
class UserBehavior(TaskSet):
    # 用百度做demo
    # @task
    # def baidu_page(self):
    #     self.client.get("/")

    def on_start(self):
        """
        on_start is called when a Locust start before any task is scheduled
        :return:
        """
        self.login()

    def login(self):
        self.client.post("/login_action",{"username":"admin", "password":"1qaz!QAZ"})

    @task(2)
    def event_manage(self):
        self.client.get("/event_manage/")

    @task(2)
    def guest_manage(self):
        self.client.get("/guest_manage/")

    @task(1)
    def search_phone(self):
        self.client.get("/search_phone",params={"phone":"13500110011"})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 6000
