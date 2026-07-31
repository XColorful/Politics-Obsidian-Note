|[马原](马原/马克思主义基本原理.md)|[思修](思修/思想道德与法治.md)|[史纲](史纲/中国近代史纲要.md)|[毛中特](毛中特/毛泽东思想和中国特色社会主义理论体系概论.md)|[新思想](新思想/习近平新时代中国特色社会主义思想概论.md)|
|:-:|:-:|:-:|:-:|:-:|
|[![马克思主义基本原理.png](./README/马克思主义基本原理.png)](马原/马克思主义基本原理.md)|[![思想道德与法治.png](./README/思想道德与法治.png)](思修/思想道德与法治.md)|[![中国近代史纲要.png](./README/中国近代史纲要.png)](史纲/中国近代史纲要.md)|[![毛泽东思想和中国特色社会主义理论体系概论.png](./README/毛泽东思想和中国特色社会主义理论体系概论.png)](毛中特/毛泽东思想和中国特色社会主义理论体系概论.md)|[![习近平新时代中国特色社会主义思想概论.png](./README/习近平新时代中国特色社会主义思想概论.png)](新思想/习近平新时代中国特色社会主义思想概论.md)|

核心考案的[Obsidian](https://obsidian.md/)笔记，粉刷[绿墙](https://github.com/XColorful)以自勉，公开[仓库](https://github.com/XColorful/Politics-Obsidian-Note)以共勉

|笔记内容|脚本|其他|
|:-:|:-:|:--|
|[马原](马原/马克思主义基本原理.md)|[Python](https://www.python.org/)|[Obsidian](https://obsidian.md/download)|
|[思修](思修/思想道德与法治.md)|[移除行首标签](移除行首标签.cmd)|[Github Desktop](https://github.com/apps/desktop)|
|[史纲](史纲/中国近代史纲要.md)|[恢复行首标签](恢复行首标签.cmd)|[笔记仓库页面](https://github.com/XColorful/Politics-Obsidian-Note)|
|[毛中特](毛中特/毛泽东思想和中国特色社会主义理论体系概论.md)|[替换首行字符串](替换首行字符串.cmd)|[笔记仓库Issue](https://github.com/XColorful/Politics-Obsidian-Note/issues)|
|[新思想](新思想/习近平新时代中国特色社会主义思想概论.md)|[SQLite 镜像](sqlite/README.md)|[笔记仓库Wiki](https://github.com/XColorful/Politics-Obsidian-Note/wiki)|

## 使用说明
> 💡我是小白，点击查看[图文教程](https://github.com/XColorful/Politics-Obsidian-Note/wiki)😀（笔记内查看[离线版教程](./Wiki/Home.md)）

### 下载笔记
1. 下载[Github Desktop](https://desktop.github.com/download/)，到[仓库页面](https://github.com/XColorful/Politics-Obsidian-Note)点击绿色的`<>Code ▼`，点击`Open with Github Desktop`
2. 下载[Obsidian](https://obsidian.md/download)，打开本地仓库（Open folder as vault），选择本地仓库目录（`Politics-Obsidian-Note`）

### 同步笔记更新

1. 打开[Github Desktop](https://github.com/apps/desktop)，点击`Fetch origin`，如有更新则点击`Pull origin`即可
2. （可选）点击`Current branch`，可以查看是否有其他分支（Branch）更新

### 个性化与协作

1. 到[仓库页面](https://github.com/XColorful/Politics-Obsidian-Note)点击`<>Code ▼`右上角的`Fork`，在自己的仓库界面[下载笔记](#下载笔记)，即可得到自己的专属版本
2. 对笔记进行修改后（如添加自己的内容、修改笔记错误等），在[Github Desktop](https://github.com/apps/desktop)里填写`Summary`、`Description`（可选）后，点击`Commit x files to xxx`即可
3. 协作（详细可以请教程序员朋友或AI）：新建分支（Branch） → 提交修改（Commit） → 点击`Create Pull Request`
4. 提出建议/对笔记有疑问/请教使用方式：到[仓库Issue](https://github.com/XColorful/Politics-Obsidian-Note/issues)点击绿色的`New issue`，描述完之后点击`Create`即可

### 脚本

#### 移除行首标签
> 临时移除所有笔记第一行的标签（如'#选择题'、'#重点'、'#非重点'等），让[关系图谱](https://publish.obsidian.md/help-zh/%E6%A0%B8%E5%BF%83%E6%8F%92%E4%BB%B6/%E5%85%B3%E7%B3%BB%E5%9B%BE%E8%B0%B1)（`Ctrl` + `G`）更纯净
1. 下载[Python](https://www.python.org/)
2. 运行仓库根目录的`移除行首标签.cmd`或`恢复行首标签.cmd`即可（笔记内快捷方式：[移除行首标签](移除行首标签.cmd)、[恢复行首标签](恢复行首标签.cmd)）

> 💡使用建议（避坑指南）：
> - 运行前：若已修改笔记，请务必先完成`Commit x files to xxx`
> - 纯查看：运行脚本查看完图谱，再`恢复行首标签`后如果[Github Desktop](https://github.com/apps/desktop)里修改没清除，则直接全选修改，右键点击`Discard changes`即可还原
> - 有修改：若在移除标签期间修改了笔记，请先运行`恢复行首标签.cmd`，确认无误后再`Commit x files to xxx`

#### SQLite 镜像
> 把所有笔记结构化导入 SQLite，方便用 SQL 抽背 / 统计标签 / 查关系图。
- 详细说明：[sqlite/README.md](sqlite/README.md)（含 schema、用法、示例查询）
- 直接查询：`sqlite3 sqlite/politics.db "..."`
- 笔记更新后重新生成：`python sqlite/sqlite_import.py`（需 Python 3.10+，仅标准库）
- 仓库自带预生成的 `sqlite/politics.db`（1.4 MB），clone 后直接可用

## 笔记展示

|[马克思主义基本原理](马原/马克思主义基本原理.md)|[考点14 主观能动性和客观规律性的辩证统一](马原/b%20马克思主义哲学/1%20辩证唯物论/考点14%20主观能动性和客观规律性的辩证统一.md)|
|:-:|:-:|
|![马原目录](./README/马原目录.png)|![主观能动性和客观规律性](./README/主观能动性和客观规律性.png)|

|[考点18 对立统一规律(唯物辩证法第一规律)](马原/b%20马克思主义哲学/2%20唯物辩证法/考点18%20对立统一规律(唯物辩证法第一规律).md)|[考点31 实践对认识的决定作用](马原/b%20马克思主义哲学/3%20认识论/考点31%20实践对认识的决定作用.md)|
|:-:|:-:|
|![对立统一规律](./README/对立统一规律.png)|![实践对认识的决定作用](./README/实践对认识的决定作用.png)|

|[考点67 剩余价值的再生产](马原/c%20马克思主义政治经济学/5%20资本主义的本质及规律/考点67%20剩余价值的生产.md)|[考点15 新民主主义社会的性质和特点](毛中特/b%20毛泽东思想/3%20社会主义改造理论/考点15%20新民主主义社会的性质和特点.md)|
|:-:|:-:|
|![三个角度分析卖包子](./README/三个角度分析卖包子.png)|![新民主主义社会五种经济成分](./README/新民主主义社会五种经济成分.png)|

|[移除行首标签](移除行首标签.cmd)|[恢复行首标签](恢复行首标签.cmd)|
|:-:|:-:|
|![移除行首标签](./README/移除行首标签.png)|![恢复行首标签](./README/恢复行首标签.png)|

|[星星之火](毛中特/b%20毛泽东思想/2%20新民主主义革命理论/考点12%20新民主主义革命的道路.md)|[可以燎原](史纲/b%20新民主主义革命时期/5%20中国革命的新道路/考点43%20农村包围城市、武装夺取政权的道路.md)|
|:-:|:-:|
|![Markdown纯文本格式](./README/星星之火.png)|![Obsidian标签、悬浮显示双链笔记](./README/可以燎原.png)|

## 在开源中相遇，在实践中改变

资源的有限不是束缚，而是我们在既定历史条件下共同出发的起点。

决定发展的从来不是孤立个体的意志，而是人们在协作实践中改变世界的方式。


“躺平”不是否定，而是一种对现实结构的无声反应。

疲惫与停滞并非个人的失败，而是社会关系中矛盾的体现；

真正的否定，来自对这些矛盾的认识与改造。



矛盾推动事物运动。

平衡只是暂时的状态，新的可能往往诞生于集体行动与结构性张力之中。



意志能给我们方向，但唯有实践能让认识扎根。

改造客观世界的过程中，人们的能动性才真正生成。



在当代数字劳动中，开源是一种社会化生产方式：

知识突破私有的围栏，协作让经验积累为共享财富。



笔记的公开不是单向输出，

而是将思想对象化，使其能够在更广阔的合作网络中流动、被扩展、被修正。



感官满足是短暂的，而知识与实践的沉淀会在共同劳动中积累为现实力量。



每一次阅读、整理与分享，都是一次“认识—实践—再认识”的循环；

个人的学习螺旋上升，也只有在知识共同体中才能获得真正的方向与意义。



拒绝原子化的孤立奋斗。

在共同生产、共同分享、共同进步中，学习不只服务于自我，

而是成为人与世界互相改变的过程。

## 授权信息 (Licensing)

许可证：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

本分支及其后续版本依据 **知识共享 署名-相同方式共享 4.0 国际协议** 授权发布。

### 您的义务

1. **署名 (BY)**：转载或二次创作须注明原作者 `XColorful` 及 [本仓库链接](https://github.com/XColorful/Politics-Obsidian-Note)。
2. **相同方式共享 (SA)**：衍生作品必须继续使用 **CC BY-SA 4.0** 协议发布。

> _注：历史版本 [Release 2025-GPLv3 · XColorful/Politics-Obsidian-Note](https://github.com/XColorful/Politics-Obsidian-Note/releases/tag/GPLv3) 仍保留 GPLv3 授权。_
