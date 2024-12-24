
CSANMT-Translation为翻译的模型服务; 项目基于**TensorFlow**框架**CSANMT**系列(Modelscope平台)的模型翻译项目; 目前支持中文到英文的翻译，英文到中文的翻译,其他模型可以到[Modelscope](https://modelscope.cn/models)下载即可. 也可以作为**FastApi**入门项目使用. 对性能有要求可以看章节性能部分参数;
本项目基于pyhton的fastapi框架开发. 代码简洁,可以直接部署作为翻译的原子(微服务)服务使用投入到生成. 特色:
- 模型预加载 - 减少首次推理时间
- 超长文本推理 - 内置切分、断句逻辑
- API封装 - 基于FastApi开箱即用,调用方式参考[API调用章节]( #API调用)

<div align="center">  
<h4>
 <a href="#安装教程"> 安装教程 </a>   
｜<a href="#训练"> 训练 </a>
｜<a href="#性能"> 性能 </a>
｜<a href="#配置及缓存"> 配置及缓存 </a>
</h4>
</div>

<a name="安装教程"></a>
## 安装教程
- 部署最简单的方式是使用docker-compose部署, 支持了GPU, CPU
- MPS, 其他Mac/Win平台开发调试,Clone本项目后直接requirments.txt安装依赖

### Docker部署
  - 1、在本地主机上安装最新版本的 Docker,自带了Compose版本。
  - 2、如需在 Linux 上启用 GPU推理，请安装显卡[NVIDIA的驱动](https://github.com/NVIDIA/nvidia-docker/wiki/Frequently-Asked-Questions#how-do-i-install-the-nvidia-driver) 以及 [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker) 支持
  以上都可以参考[TensorFlow](https://www.tensorflow.org/install/docker?hl=zh-cn)官网文档。
  - 3、修改模型、日志挂载目录等配置,具体可以参考docker-compose.yml文件;
  - 4、运行 docker-compose.yml
      ```bash
      docker compose up -d --build
      ```
    
  - 5、镜像 && 核心的组件
    - 镜像:tensorflow/tensorflow:2.18.0-gpu,需要其他镜像可以到dockerhub上自行更新/更换;如果更新/更换镜像注意涉及相应pip依赖保持更新.以下为镜像里核心组件的版本号,你也可以自行到官方镜像具体查询.
      - CUDA_VERSION=12.3.0
      - PYTHON_VERSION=python3.11
      - TENSORFLOW_PACKAGE=tensorflow==2.18.0
  
    - python包核心依赖:
      - torch_tensorrt==2.2.0 (linux的GPU必须依赖; 这个在modelscope平台里没有具体说明的核心)
      - modelscope==1.21.0
      - datasets==2.18.0
      - sacremoses==0.1.1
      - subword_nmt==0.3.8
        其他依赖在requirements.txt中
### 本地开发部署
- 要求**python>3.10**; 直接pip install -r requirements.txt后启动即可
    ```bash
    pip install --default-timeout=600 -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
    ```
### 更换模型
- 目前预置为modelscope的两个模型.路径在tanslation.translation.ModelEnum.model_path; 自行更换即可

    ```bash
       class ModelEnum(Enum):
           ZH2EN = ModelConfig(model_path="damo/nlp_csanmt_translation_zh2en", preload_infer_text="你好",
                               split_pattern=r"[。！？；]")
           EN2ZH = ModelConfig(model_path="damo/nlp_csanmt_translation_en2zh", preload_infer_text="hello",
                               split_pattern=r"[.!?;,]")
    ```

### API调用
- 启动后,默认端口为11000,可以通过修改docker-compose.yml中的ports参数来修改端口;
 
例子:中文 =》英文
```bash 
curl --location '127.0.0.1:11000/translation' \
--header 'Content-Type: application/json' \
--data '{
    "text":"沉睡数千年, 一醒惊天下. 你好欢迎来到三星堆博物馆.",
    "source_lang":"zh",
    "target_lang":"en"
}'
```
将的到如下结果:

```json
{
    "errorcode": 0,
    "ret": 0,
    "msg": "ok",
    "traceid": "",
    "data": "Sleeping for thousands of years, waking up to shock the world. Hello and welcome to Sanxingdui Museum."
}
```

例子:英文=》中文

```bash 
curl --location '127.0.0.1:11000/translation' \
--header 'Content-Type: application/json' \
--data '{
    "text":"Sleeping for thousands of years, waking up to shock the world. Hello and welcome to Sanxingdui Museum.",
    "source_lang":"en",
    "target_lang":"zh"
}'
 ```
返回结果:
```json
{
    "errorcode": 0,
    "ret": 0,
    "msg": "ok",
    "traceid": "",
    "data": "睡了几千年，醒来震惊世界。大家好，欢迎来到三星堆博物馆。"
}
```



<a name="训练"></a>
## 训练
- 模型微调/训练,请参考官方[Modelscope](https://www.modelscope.cn/models/iic/nlp_csanmt_translation_zh2en)文档

<a name="性能"></a>
## 性能
- 模型大小: large-7GB
- 各平台推理性能测试:

| 设备                        | 推理速度 (ms)-10个字(中文)/单词(英文) | 推理速度(ms)-20个字(中文)/单词(英文) |
|-----------------------------|---------------------------|--------------------------|
| **CPU (8C/16G)**            | 2000 ~ 3000 ms            | 3000 ~ 4000 ms           |
| **RTX-4090 / Tesla-P40 / RTX-3060Ti** | 100 ~ 200 ms              | 200 ~ 400 ms             |
| **MPS**                     | 100 ~ 200 ms              | 200 ~ 400 ms             |

 通过多个GPU来测试, 对于**单次**推理速度基本都差不多. 如果有负载好的显卡对于承载会更高;

<a name="配置及缓存"></a>
## 配置及缓存：
- 模型缓存目录: ~/.cache/modelscope/hub/下; 通过挂载到主机,主机目录可以docker-compose.yml修改
- 日志目录: /app/logs下;通过挂载到主机,主机目录可以docker-compose.yml修改

## 许可协议
项目遵循[The MIT License](https://opensource.org/licenses/MIT)开源协议，模型许可协议请参考（[模型协议](./MODEL_LICENSE)）

## 引用

``` bibtex
@inproceedings{wei-etal-2022-learning,
  title = {Learning to Generalize to More: Continuous Semantic Augmentation for Neural Machine Translation},
  author = {Xiangpeng Wei and Heng Yu and Yue Hu and Rongxiang Weng and Weihua Luo and Rong Jin},
  booktitle = {Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics, ACL 2022},
  year = {2022},
}
```
