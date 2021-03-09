# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Any

from utils.component import BaseHandler
import yaml
import os


class UpgradeImage(BaseHandler):

    def __init__(self):
        self.base_path = None
        self.product_name = None
        self.product_path = None
        self.product_version = None
        self.file_path = None
        self.manifest = None

    def parse_args(self, args: list):
        if len(args) < 3:
            msg = "Please check the args num[{}], should > 3".format(len(args))
            raise KeyError(msg)

        self.product_name = args[0]
        self.manifest = args[1]
        self.product_version = args[2]

        base_path = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../.."))
        self.base_path = os.path.join(base_path, "k8s-template")
        self.get_product_path(self.base_path)

    def get_product_path(self, path):
        for c_dir in os.listdir(path):
            c_path = os.path.join(path, c_dir)
            if not os.path.isdir(c_path):
                continue
            if c_dir == self.product_name:
                self.product_path = c_path
                break
            self.get_product_path(c_path)

    def pre_check(self) -> None:
        # check whether exist the product in coding-template
        if self.product_path is None:
            msg = "Cant`t find the product[{}], please the product_name.".format(self.product_name)
            raise KeyError(msg)

        # check whether exist the manifest for kubernetes
        if self.manifest is None:
            msg = "Miss the manifest[{}]".format(self.manifest)
            raise ValueError(msg)

        # check whether exist the product version for docker image's tag
        if self.manifest is None:
            msg = "Miss the product version[{}]".format(self.manifest)
            raise ValueError(msg)

        file_list = [i for i in os.listdir(self.product_path) if "%s.yaml" % self.manifest == i]
        if len(file_list) == 0:
            msg = "Can't find the aim manifest[{}]".format(self.manifest)
            raise ValueError(msg)
        self.file_path = os.path.join(self.product_path, file_list[0])

    def run_module(self, args: list):
        self.parse_args(args)
        self.pre_check()

        with open(self.file_path, "r", encoding="utf-8") as mf:
            d_mf = yaml.load(mf, Loader=yaml.FullLoader)
        print("Image_B:", d_mf["spec"]["template"]["spec"]["containers"][0]["image"])
        self.update_value(d_mf, self.product_version)
        print("Image_A:", d_mf["spec"]["template"]["spec"]["containers"][0]["image"])

        mf = open(self.file_path, "w", encoding="utf-8")
        yaml.dump(d_mf, mf)
        mf.close()

    def update_value(self, d_mf: Any, value: Any) -> None:
        if self.manifest in ("deployment", "statefulset"):
            containers = d_mf["spec"]["template"]["spec"]["containers"]
            for con in containers:
                image = con["image"]
                image_split = image.split("/")
                if ":" in image_split[-1]:
                    image_name = image_split[-1].split(":")[0]
                    image_split[-1] = image_name+":"+self.product_version
                    image = "/".join(image_split)
                else:
                    image = image + ":" + self.product_version
                con["image"] = image

    def notes(self) -> str:
        return "\tUpdate the docker image version for manifest"


if __name__ == "__main__":
    n = ["svn-server", "statefulset", "v1"]

    UpgradeImage().run_module(n)