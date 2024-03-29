# グラフ作成に関するプログラム

import json
import os

import japanize_matplotlib
import matplotlib.pyplot as plt
from Dango_Analyzer.utils.csv_preprocessing import CSVProcess
from PIL import Image


class Graph(CSVProcess):

   def all_body_plot(self, csv_path, file_name, parts, width, height, likelihood):  # すべてのパーツをプロット
      self.preprocessing(csv_path)
      fig = plt.figure()
      ax = fig.add_subplot(1, 1, 1, aspect="equal")
      cm = plt.cm.get_cmap("rainbow")
      for i, column in enumerate(parts):
         number = self.legends.index(column)
         rgb = cm(number / len(self.legends))
         print(rgb)
         x_tmp = []
         y_tmp = []
         for i, j in enumerate(self.neighborhood[column]):
            if j >= likelihood:
               x_tmp.append(self.x[column][i])
               y_tmp.append(self.y[column][i])

         ax.scatter(x_tmp, y_tmp, s=30, alpha=0.5, label=column, color=rgb)
         ax.set_xlim(0, width)
         ax.set_ylim(0, height)
         ax.invert_yaxis()
         plt.xlabel("x[pixel]", size="large", color="green")
         plt.ylabel("y[pixel]", size="large", color="blue")
         plt.legend(loc='best',
                    bbox_to_anchor=(1, 1),
                    borderaxespad=0.,)
      output_path = csv_path.split(os.path.basename(csv_path))[0]
      plt.savefig(f"{output_path}/{file_name}", dpi=500, bbox_inches='tight')

   def frame_x_y(self, ax, colors, legs, part):
      if part == 1:
         for i, column in enumerate(legs[0:7]):
            ax.plot(self.frames_num, self.x[column], linewidth=2, c=colors[i], label=column + "_x")
         for i, column in enumerate(legs[0:7]):
            ax.plot(self.frames_num, self.y[column], linewidth=2, c=colors[i], linestyle="dashed", label=column + "_y")
      else:
         for i, column in enumerate(legs[7:14]):
            ax.plot(self.frames_num, self.x[column], linewidth=2, c=colors[i + 7], label=column + "_x")
         for i, column in enumerate(legs[7:14]):
            ax.plot(self.frames_num, self.y[column], linewidth=2, c=colors[i + 7], linestyle="dashed", label=column + "_y")
      return ax

   def frame_x_y2(self, ax, colors, legs, part, num):
      self.plots_data.append(self.frames_num[num])
      if part == 1:
         for i, column in enumerate(legs[0:7]):
            if column not in self.animation_x:
               self.animation_x[column] = self.x[column][0:num + 1]
            else:
               self.animation_x[column].append(self.x[column][0:num + 1])
            print(self.plots_data, self.animation_x[column])
            ax.plot(self.plots_data, self.animation_x[column], linewidth=2, c=colors[i], label=column + "_x")
         for i, column in enumerate(legs[0:7]):
            if column not in self.animation_y:
               self.animation_y[column] = self.y[column][0:num + 1]
            else:
               self.animation_y[column].append(self.y[column][0:num + 1])
            ax.plot(self.plots_data, self.animation_y[column], linewidth=2, c=colors[i], label=column + "_x")
      else:
         for i, column in enumerate(legs[7:14]):
            ax.plot([self.frames_num[num]], [self.x[column][num]], linewidth=2, c=colors[i + 7], label=column + "_x")
         for i, column in enumerate(legs[7:14]):
            ax.plot([self.frames_num[num]], [self.y[column][num]], linewidth=2, c=colors[i + 7], linestyle="dashed", label=column + "_y")
      return ax

   def frame_plot(self):
      fig = plt.figure()
      plt.rcParams['figure.figsize'] = (20, 5)
      with open("util.json", "r")as f:
         util = json.load(f)
      colors = util["rolylegs_colors"]
      legs = util["14legs_dactylus"]
      ax = fig.add_subplot(1, 1, 1)
      ax.set_xlim(0, 10000)
      ax.set_ylim(0, 1280)
      part = 2
      ax = self.frame_x_y(ax, colors, legs, part)
      plt.xlabel("Frame Index", size="large", color="green")
      plt.ylabel("x(soild),y(dashed)[pixel]", size="large", color="blue")
      plt.legend(loc='best',
                 bbox_to_anchor=(1, 1),
                 borderaxespad=0.,)
      try:
         plt.savefig(f"images/{self.path}/{self.path}_frame{part}.png", dpi=500, bbox_inches='tight')
      except FileNotFoundError:
         os.mkdir(f"images/{self.path}")
         plt.savefig(f"images/{self.path}/{self.path}_frame{part}.png", dpi=500, bbox_inches='tight')

   def midi(self):
      im = Image.open(f"images/{self.path}/haimen.jpg")
      fig = plt.figure()
      with open("util.json", "r")as f:
         dic = json.load(f)
      haimen = dic["haimen_dango"]
      colors = dic["rolylegs_colors"]
      ax = fig.add_subplot(1, 1, 1)
      ax.imshow(im, alpha=0.6)
      ax.set_xlim(0, 2160)
      ax.set_ylim(0, 3840)
      cen_x = (self.x["tail"][0] + self.x["head"][0]) / 2
      cen_y = (self.y["tail"][0] + self.y["head"][0]) / 2
      ax.scatter(self.x["head"][0], self.y["head"][0], s=30, alpha=0.5, c="blue", label="head")
      ax.scatter(self.x["tail"][0], self.y["tail"][0], s=30, alpha=0.5, c="blue", label="tail")
      ax.scatter(cen_x, cen_y, s=30, alpha=0.5, c="blue", label="center")
      plt.xlabel("Frame Index", size="large", color="green")
      plt.ylabel("x(soild),y(dashed)[pixel]", size="large", color="blue")
      plt.legend(loc='best',
                 bbox_to_anchor=(1, 1),
                 borderaxespad=0.,)
      try:
         plt.savefig(f"images/{self.path}/{self.path}_frame.png", dpi=500, bbox_inches='tight')
      except FileNotFoundError:
         os.mkdir(f"images/{self.path}")
         plt.savefig(f"images/{self.path}/{self.path}_frame.png", dpi=500, bbox_inches='tight')

   def frame_plot2(self):
      fig = plt.figure()
      plt.rcParams['figure.figsize'] = (20, 5)
      with open("util.json", "r")as f:
         util = json.load(f)
      colors = util["rolylegs_colors"]
      legs = util["14legs_dactylus"]

      for i in range(len(self.frames_num)):
         fig = plt.figure()
         ax = fig.add_subplot(1, 1, 1)
         ax.set_xlim(0, 10000)
         ax.set_ylim(0, 1280)
         part = 1
         ax = self.frame_x_y2(ax, colors, legs, part, i)
         plt.xlabel("Frame Index", size="large", color="green")
         plt.ylabel("x(soild),y(dashed)[pixel]", size="large", color="blue")
         plt.legend(loc='best',
                    bbox_to_anchor=(1, 1),
                    borderaxespad=0.,)
         try:
            plt.savefig(f"images/{self.path}/{self.path}flames/{self.path}_frame{i}.png", dpi=500, bbox_inches='tight')
         except FileNotFoundError:
            os.mkdir(f"images/{self.path}/{self.path}flames")
            plt.savefig(f"images/{self.path}/{self.path}flames/{self.path}_frame{i}.png", dpi=500, bbox_inches='tight')


if __name__ == "__main__":
   Analayze = Graph()
   Analayze.main()
