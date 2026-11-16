#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 6 个科研流程模板注入军机处看板旨库（dashboard/dashboard.html）。

用法（项目根目录）：
    python scripts/add_research_templates.py

幂等：已注入则跳过，可重复执行。
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
TARGET = REPO / 'dashboard' / 'dashboard.html'
ANCHOR = 'const TEMPLATES = ['
MARKER = "id:'tpl-research-project'"

RESEARCH_TEMPLATES = """  {id:'tpl-research-project', cat:'科研流程', icon:'🔬', name:'科研立项（完整流程）',
   desc:'按八阶段六道门禁推进完整研究项目：立项→调研→开题→实验→分析→写作→内审→投稿归档',
   depts:['中书省','门下省','尚书省','户部','兵部','礼部','刑部'], est:'~数天(分阶段)', cost:'按阶段核算',
   params:[
     {key:'topic', label:'研究课题', type:'textarea', required:true},
     {key:'goal', label:'目标产出', type:'select', options:['可投稿论文','研究报告','实验复现'], default:'可投稿论文'},
     {key:'field', label:'所属领域', type:'text', default:'人工智能'},
     {key:'budget', label:'资源约束（算力/时间）', type:'text', default:'常规算力，两周内'}
   ],
   command:'圣旨：立项研究「{topic}」（领域：{field}），按完整科研流程推进，目标产出：{goal}。资源约束：{budget}。要求：中书省先完成选题论证与立项建议书，过门下省 G1 评审后逐阶段推进，每道门禁通过方可进入下一阶段。'},
  {id:'tpl-literature-review', cat:'科研流程', icon:'📚', name:'文献综述',
   desc:'户部主导文献检索与调研，确认研究空白，门下省 G2 评审后产出调研报告',
   depts:['户部','中书省','门下省'], est:'~40分钟', cost:'¥3',
   params:[
     {key:'field', label:'调研领域/主题', type:'textarea', required:true},
     {key:'years', label:'时间范围', type:'select', options:['近1年','近3年','近5年','不限'], default:'近3年'},
     {key:'count', label:'目标文献数量', type:'text', default:'30'},
     {key:'format', label:'输出格式', type:'select', options:['Markdown报告','结构化清单+报告'], default:'结构化清单+报告'}
   ],
   command:'圣旨：对「{field}」做文献调研（范围：{years}，目标 {count} 篇），户部按 SOP-2 执行：结构化文献清单（全部引用真实可溯源）、流派分类、≥3 篇最相关工作对比、研究空白陈述，产出{format}，提交门下省 G2 评审。'},
  {id:'tpl-proposal', cat:'科研流程', icon:'📋', name:'开题报告',
   desc:'中书省组织兵部/户部/工部会签，产出含假设、实验设计、里程碑的开题报告，过 G3 评审',
   depts:['中书省','门下省','兵部','户部','工部'], est:'~60分钟', cost:'¥4',
   params:[
     {key:'topic', label:'研究课题', type:'textarea', required:true},
     {key:'hypothesis', label:'初步研究假设（可选）', type:'text', default:''},
     {key:'resource', label:'实验资源', type:'text', default:'常规算力'}
   ],
   command:'圣旨：为课题「{topic}」起草开题报告。初步假设：{hypothesis}（如为空由中书省拟定）。资源：{resource}。按 SOP-3 执行：可检验假设、基线/对照实验设计（兵部）、数据与统计方案（户部）、环境方案（工部）、评估指标、里程碑、风险与回退方案，提交门下省 G3 评审，未通过不得开工实验。'},
  {id:'tpl-reproduction', cat:'科研流程', icon:'🧪', name:'实验复现',
   desc:'兵部复现指定论文/方法，工部保环境，刑部做可复现性审计',
   depts:['兵部','工部','刑部','尚书省'], est:'~半天', cost:'¥5',
   params:[
     {key:'paper', label:'论文标题/链接', type:'textarea', required:true},
     {key:'env', label:'复现环境', type:'select', options:['Python/PyTorch','Python/其他','按原文环境'], default:'按原文环境'},
     {key:'scope', label:'复现范围', type:'select', options:['主结果','主结果+消融','全部实验'], default:'主结果'}
   ],
   command:'圣旨：复现「{paper}」，范围：{scope}，环境：{env}。工部搭建并冻结环境，兵部按简化开题执行并留完整实验记录，户部核对数据一致性，刑部做可复现性审计并出具报告。失败实验同样记录归因。'},
  {id:'tpl-paper-writing', cat:'科研流程', icon:'✍️', name:'论文写作与内审',
   desc:'礼部基于项目成果撰写论文初稿，门下省 G5 写作内审后修改定稿',
   depts:['礼部','门下省','户部','兵部'], est:'~90分钟', cost:'¥6',
   params:[
     {key:'project', label:'课题/已有成果概述', type:'textarea', required:true},
     {key:'venue', label:'目标 venue', type:'text', default:'通用学术格式'},
     {key:'lang', label:'写作语言', type:'select', options:['中文','英文'], default:'中文'}
   ],
   command:'圣旨：基于「{project}」的成果撰写论文初稿（目标：{venue}，语言：{lang}）。礼部按 SOP-6 执行：先出一页故事线，再写全结构初稿，图表自明、引用与文献清单一致、无夸大表述、写明局限性，提交门下省 G5 写作内审并逐条修改。'},
  {id:'tpl-peer-review', cat:'科研流程', icon:'⚖️', name:'投稿前评审（G6 双签）',
   desc:'门下省模拟同行评审 + 刑部诚信合规终审，双签通过后产出投稿包',
   depts:['门下省','刑部','礼部'], est:'~45分钟', cost:'¥3',
   params:[
     {key:'manuscript', label:'稿件/项目说明', type:'textarea', required:true},
     {key:'strictness', label:'评审严格度', type:'select', options:['顶会标准','一般期刊标准','内部预演'], default:'顶会标准'}
   ],
   command:'圣旨：对「{manuscript}」执行 G6 投稿评审（{strictness}）。门下省以挑剔审稿人视角模拟同行评审，按接收/小修/大修/拒稿给出结论与具体意见；刑部终审引用真实性、原创性、数据一致性、可复现性与伦理合规。双签通过后礼部准备投稿包（正文/附录/图表源文件/可复现材料/投稿信/合规审计报告）。'},
"""


def main() -> int:
    if not TARGET.exists():
        print(f'[错误] 未找到 {TARGET}', flush=True)
        return 1
    html = TARGET.read_text(encoding='utf-8-sig')
    if MARKER in html:
        print('[跳过] 科研模板已存在，无需重复注入', flush=True)
        return 0
    if ANCHOR not in html:
        print(f'[错误] 未找到模板数组锚点：{ANCHOR}', flush=True)
        return 1
    html = html.replace(ANCHOR, ANCHOR + '\n' + RESEARCH_TEMPLATES, 1)
    TARGET.write_text(html, encoding='utf-8')
    print('[完成] 已注入 6 个科研流程模板，刷新看板 → 旨库 → 科研流程 即可使用', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
