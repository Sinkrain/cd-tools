# -*- coding: utf-8 -*-

from __future__ import annotations
from utils.component import UpgradeImage
import traceback
import sys


class Main:

    def __init__(self, args: list) -> None:
        self.args = args
        self.func_name = None
        self.route_map = dict()
        self.options_map = dict()
        self.generate_route()
        self.parse_args()
        self.run_module()

    def parse_args(self):
        self.func_name = self.args[0].split("/")[-1]

    def check_module(self, module: str):
        if self.route_map.get(module) is None:
            print("\n{0} is not in Commands\nSee {1} --help".format(module, self.func_name))

    def run_module(self):
        """
        module product manifest
        :return:
        """
        try:
            self.check_module(self.args[1])
            self.route_map[self.args[1]]().run_module(self.args[2:])

        except Exception as e:
            print("Error: ", e)
            print(traceback.format_exc())

    def generate_route(self):
        self.route_map["upgrade_image"] = UpgradeImage

    def _options(self):
        self.options_map["-h"] = self.notes

    def notes(self) -> None:
        print("\nUsage: {}\t[Options]\tCommands".format(self.args[0].split("/")[-1]))
        print("\nOptions:")
        for k, v in self.options_map.items():
            print("\t{}\t{}".format(k, v()))
        print("\nCommands:")
        for k, v in self.route_map.items():
            print("\t{}\t{}".format(k, v().notes()))


if __name__ == "__main__":
    input_args = sys.argv
    # Just for test
    # input_args = ["main.py", "upgrade_image", "e-coding", "deployment", "v1"]
    main = Main(input_args)
