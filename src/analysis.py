"""第19讲 拓展：评论文本与规则式主题分析
业务问题：评分之外，顾客提到了哪些具体问题？
全部使用模拟教学数据。"""
from pathlib import Path
import sys
if "__file__" in globals():
    COURSE_ROOT = Path(__file__).resolve().parents[1]
else:
    COURSE_ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "course_common.py").exists())
if str(COURSE_ROOT) not in sys.path:
    sys.path.insert(0, str(COURSE_ROOT))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from course_common import (ROOT, DATA, AS_OF, BLUE, TEAL, ORANGE, load_tables,
    build_facts, positive_orders, rfm_table, safe_divide, outdir, save_table, save_figure, show)

import re
# %% 透明的关键词多标签：一条评论可以命中多个主题
reviews=load_tables()['reviews'].copy()
themes={'物流':['物流','发货'],'质量':['质量','破损'],'服务':['客服','服务'],'价格':['价格','性价比'],'包装':['包装']}
for theme,words in themes.items():
    pattern='|'.join(re.escape(w) for w in words)
    reviews[theme]=reviews.review_text.str.contains(pattern,regex=True,na=False)
report=pd.DataFrame([{'theme':theme,'matched_reviews':int(reviews[theme].sum()),
    'share':reviews[theme].mean(),'low_rating_share_within_theme':reviews.loc[reviews[theme],'rating'].le(2).mean()} for theme in themes])
show(report);save_table(report,19,'review_theme_summary');save_table(reviews,19,'review_tags')
fig,ax=plt.subplots(figsize=(7,4));ax.bar(report.theme,report.share*100,color=TEAL)
ax.set(title='Keyword themes in fictional reviews',ylabel='Reviews mentioning theme (%)');save_figure(fig,19,'review_themes')
print('所有评论都是教学模板；“质量”可能出现在表扬和批评中，关键词主题不等于情感标签，比例之和可超过100%。')
