#!/usr/bin/env python3
"""IELTS daily content generator. Run daily via GitHub Actions."""
import json, os, random, hashlib

BASE = os.path.dirname(os.path.abspath(__file__))

# ── Word banks (80+ per theme) ──────────────────────────────────────────
WORDS = {
  "education": [
    {"word":"academic","phonetic":"/ˌækəˈdemɪk/","meaning":"adj. 学术的","example":"She pursued an academic career in linguistics.","exampleCn":"她从事语言学学术生涯。"},
    {"word":"curriculum","phonetic":"/kəˈrɪkjələm/","meaning":"n. 课程","example":"The curriculum was redesigned to include coding.","exampleCn":"课程被重新设计以包含编程。"},
    {"word":"compulsory","phonetic":"/kəmˈpʌlsəri/","meaning":"adj. 强制的，必修的","example":"Physical education is compulsory in most schools.","exampleCn":"体育在大多数学校是必修的。"},
    {"word":"assessment","phonetic":"/əˈsesmənt/","meaning":"n. 评估","example":"Teachers use various forms of assessment.","exampleCn":"教师使用多种评估方式。"},
    {"word":"pedagogy","phonetic":"/ˈpedəɡɒdʒi/","meaning":"n. 教学法","example":"Modern pedagogy focuses on critical thinking.","exampleCn":"现代教学法注重批判性思维。"},
    {"word":"literacy","phonetic":"/ˈlɪtərəsi/","meaning":"n. 读写能力","example":"Digital literacy is as important as traditional literacy.","exampleCn":"数字素养与传统读写能力同等重要。"},
    {"word":"tuition","phonetic":"/tjuˈɪʃn/","meaning":"n. 学费","example":"Rising tuition costs burden many families.","exampleCn":"上涨的学费给许多家庭带来负担。"},
    {"word":"scholarship","phonetic":"/ˈskɒləʃɪp/","meaning":"n. 奖学金","example":"She earned a full scholarship to study abroad.","exampleCn":"她获得了全额奖学金出国学习。"},
    {"word":"vocational","phonetic":"/vəʊˈkeɪʃənl/","meaning":"adj. 职业的","example":"Vocational training offers practical skills.","exampleCn":"职业培训提供实用技能。"},
    {"word":"competence","phonetic":"/ˈkɒmpɪtəns/","meaning":"n. 能力","example":"Employers value both knowledge and competence.","exampleCn":"雇主重视知识和能力。"},
    {"word":"enrolment","phonetic":"/ɪnˈrəʊlmənt/","meaning":"n. 注册，入学","example":"Enrolment in STEM courses has increased.","exampleCn":"STEM课程注册人数增加了。"},
    {"word":"discipline","phonetic":"/ˈdɪsəplɪn/","meaning":"n. 纪律；学科","example":"Classroom discipline creates an effective environment.","exampleCn":"课堂纪律创造有效的学习环境。"},
    {"word":"graduate","phonetic":"/ˈɡrædʒuət/","meaning":"n./v. 毕业生；毕业","example":"Graduates face a competitive job market.","exampleCn":"毕业生面临竞争激烈的就业市场。"},
    {"word":"illiterate","phonetic":"/ɪˈlɪtərət/","meaning":"adj. 文盲的","example":"Efforts continue to reduce illiterate populations.","exampleCn":"继续努力减少文盲人口。"},
    {"word":"mentor","phonetic":"/ˈmentɔːr/","meaning":"n. 导师","example":"A good mentor can shape a student's future.","exampleCn":"好的导师能塑造学生的未来。"},
    {"word":"nurture","phonetic":"/ˈnɜːtʃər/","meaning":"v. 培养","example":"Teachers should nurture curiosity in students.","exampleCn":"教师应培养学生好奇心。"},
    {"word":"plagiarism","phonetic":"/ˈpleɪdʒərɪzəm/","meaning":"n. 剽窃","example":"Plagiarism can result in severe penalties.","exampleCn":"剽窃可能导致严厉处罚。"},
    {"word":"seminar","phonetic":"/ˈsemɪnɑːr/","meaning":"n. 研讨会","example":"Weekly seminars encourage in-depth discussion.","exampleCn":"每周研讨会鼓励深入讨论。"},
    {"word":"syllabus","phonetic":"/ˈsɪləbəs/","meaning":"n. 教学大纲","example":"The syllabus outlines all course requirements.","exampleCn":"教学大纲列出了所有课程要求。"},
    {"word":"tertiary","phonetic":"/ˈtɜːʃəri/","meaning":"adj. 高等教育的","example":"Tertiary education opens up more opportunities.","exampleCn":"高等教育打开更多机会。"},
    {"word":"undergraduate","phonetic":"/ˌʌndəˈɡrædʒuət/","meaning":"n. 本科生","example":"Undergraduate programs typically last three years.","exampleCn":"本科课程通常为三年。"},
    {"word":"specialize","phonetic":"/ˈspeʃəlaɪz/","meaning":"v. 专攻","example":"Students can specialize in their second year.","exampleCn":"学生可以在第二年专攻。"},
    {"word":"dedicate","phonetic":"/ˈdedɪkeɪt/","meaning":"v. 致力于","example":"She dedicated herself to improving education.","exampleCn":"她致力于改善教育。"},
    {"word":"cognitive","phonetic":"/ˈkɒɡnətɪv/","meaning":"adj. 认知的","example":"Early education boosts cognitive development.","exampleCn":"早期教育促进认知发展。"},
    {"word":"allocate","phonetic":"/ˈæləkeɪt/","meaning":"v. 分配","example":"More funds should be allocated to schools.","exampleCn":"更多资金应分配给学校。"},
    {"word":"comprehensive","phonetic":"/ˌkɒmprɪˈhensɪv/","meaning":"adj. 全面的","example":"A comprehensive education covers many fields.","exampleCn":"全面的教育涵盖多个领域。"},
    {"word":"facilitate","phonetic":"/fəˈsɪlɪteɪt/","meaning":"v. 促进","example":"Technology can facilitate personalized learning.","exampleCn":"技术可以促进个性化学习。"},
    {"word":"innovation","phonetic":"/ˌɪnəˈveɪʃn/","meaning":"n. 创新","example":"Educational innovation transforms classrooms.","exampleCn":"教育创新改变课堂。"},
    {"word":"interactive","phonetic":"/ˌɪntərˈæktɪv/","meaning":"adj. 互动的","example":"Interactive methods engage students more effectively.","exampleCn":"互动方法更有效吸引学生。"},
    {"word":"motivation","phonetic":"/ˌməʊtɪˈveɪʃn/","meaning":"n. 动力","example":"Intrinsic motivation is key to success.","exampleCn":"内在动力是成功的关键。"},
    {"word":"phenomenon","phonetic":"/fəˈnɒmɪnən/","meaning":"n. 现象","example":"Lifelong learning is a growing phenomenon.","exampleCn":"终身学习是日益增长的现象。"},
    {"word":"potential","phonetic":"/pəˈtenʃl/","meaning":"n./adj. 潜力","example":"Every student has unique potential.","exampleCn":"每个学生都有独特的潜力。"},
    {"word":"rigorous","phonetic":"/ˈrɪɡərəs/","meaning":"adj. 严格的","example":"The program provides rigorous training.","exampleCn":"该计划提供严格的训练。"},
    {"word":"stimulate","phonetic":"/ˈstɪmjuleɪt/","meaning":"v. 激发","example":"Good teachers stimulate intellectual curiosity.","exampleCn":"好老师激发求知欲。"},
    {"word":"supplement","phonetic":"/ˈsʌplɪmənt/","meaning":"v./n. 补充","example":"Online courses supplement traditional learning.","exampleCn":"在线课程补充传统学习。"},
    {"word":"conventional","phonetic":"/kənˈvenʃənl/","meaning":"adj. 传统的","example":"Conventional methods are being re-evaluated.","exampleCn":"传统方法正在被重新评估。"},
    {"word":"inequality","phonetic":"/ˌɪnɪˈkwɒləti/","meaning":"n. 不平等","example":"Educational inequality remains a challenge.","exampleCn":"教育不平等仍是一个挑战。"},
    {"word":"diverse","phonetic":"/daɪˈvɜːs/","meaning":"adj. 多样的","example":"A diverse classroom benefits all learners.","exampleCn":"多样化的课堂使所有学习者受益。"},
    {"word":"retention","phonetic":"/rɪˈtenʃn/","meaning":"n. 保持，记忆","example":"Active learning improves knowledge retention.","exampleCn":"主动学习提高知识保持率。"},
    {"word":"curriculum vitae","phonetic":"/kəˌrɪkjələm ˈviːtaɪ/","meaning":"n. 简历","example":"A strong CV is essential for job seekers.","exampleCn":"一份好的简历对求职者至关重要。"},
    {"word":"kindergarten","phonetic":"/ˈkɪndəɡɑːtn/","meaning":"n. 幼儿园","example":"Kindergarten lays the foundation for learning.","exampleCn":"幼儿园为学习打下基础。"},
    {"word":"didactic","phonetic":"/daɪˈdæktɪk/","meaning":"adj. 教导的，说教的","example":"Didactic teaching methods have both merits and drawbacks.","exampleCn":"说教式教学方法既有优点也有缺点。"},
    {"word":"expel","phonetic":"/ɪkˈspel/","meaning":"v. 开除","example":"Schools rarely expel students except for severe cases.","exampleCn":"学校很少开除学生除非情况严重。"},
    {"word":"matriculation","phonetic":"/məˌtrɪkjuˈleɪʃn/","meaning":"n. 入学","example":"Matriculation requirements vary by institution.","exampleCn":"入学要求因学校而异。"},
    {"word":"pedagogue","phonetic":"/ˈpedəɡɒɡ/","meaning":"n. 教师，教育者","example":"Every pedagogue strives to inspire their students.","exampleCn":"每位教育者都努力激励学生。"},
    {"word":"prodigy","phonetic":"/ˈprɒdədʒi/","meaning":"n. 天才，神童","example":"The child prodigy entered university at age twelve.","exampleCn":"这位神童十二岁进入大学。"},
    {"word":"didacticism","phonetic":"/daɪˈdæktɪsɪzəm/","meaning":"n. 教导主义","example":"Modern education moves away from pure didacticism.","exampleCn":"现代教育正在摆脱纯粹的教导主义。"},
    {"word":"erudite","phonetic":"/ˈerudaɪt/","meaning":"adj. 博学的","example":"The erudite professor was respected by all.","exampleCn":"这位博学的教授受到所有人尊敬。"},
    {"word":"pedantic","phonetic":"/pɪˈdæntɪk/","meaning":"adj. 迂腐的，卖弄学问的","example":"A pedantic approach can stifle student creativity.","exampleCn":"迂腐的方法会扼杀学生的创造力。"},
    {"word":"syllabus","phonetic":"/ˈsɪləbəs/","meaning":"n. 教学大纲","example":"The syllabus is updated annually to reflect changes.","exampleCn":"教学大纲每年更新以反映变化。"},
    {"word":"didactic","phonetic":"/daɪˈdæktɪk/","meaning":"adj. 教学的","example":"Didactic materials support structured learning.","exampleCn":"教学材料支持结构化学习。"},
    {"word":"holistic","phonetic":"/həʊˈlɪstɪk/","meaning":"adj. 全面的，整体的","example":"A holistic approach to education considers emotional growth.","exampleCn":"全面的教育方法考虑情感成长。"},
    {"word":"pedagogical","phonetic":"/ˌpedəˈɡɒdʒɪkl/","meaning":"adj. 教学法的","example":"New pedagogical strategies improve student outcomes.","exampleCn":"新的教学策略改善学生成绩。"},
    {"word":"remedial","phonetic":"/rɪˈmiːdiəl/","meaning":"adj. 补习的， remedial","example":"Remedial classes help struggling students catch up.","exampleCn":"补习班帮助有困难的学生赶上来。"},
    {"word":"rote","phonetic":"/rəʊt/","meaning":"n. 死记硬背","example":"Rote learning is less effective than understanding concepts.","exampleCn":"死记硬背不如理解概念有效。"},
    {"word":"streaming","phonetic":"/ˈstriːmɪŋ/","meaning":"n. 分班，分流","example":"Streaming allows students to learn at their own pace.","exampleCn":"分班让学生按自己的节奏学习。"},
    {"word":"co-curricular","phonetic":"/ˌkəʊ kəˈrɪkjələ/","meaning":"adj. 课外辅助的","example":"Co-curricular activities complement academic learning.","exampleCn":"课外辅助活动补充学术学习。"},
  ],
  "environment": [
    {"word":"sustainable","phonetic":"/səˈsteɪnəbl/","meaning":"adj. 可持续的","example":"Sustainable practices are vital for the planet.","exampleCn":"可持续实践对地球至关重要。"},
    {"word":"conservation","phonetic":"/ˌkɒnsəˈveɪʃn/","meaning":"n. 保护","example":"Conservation programs protect endangered species.","exampleCn":"保护项目保护濒危物种。"},
    {"word":"emission","phonetic":"/ɪˈmɪʃn/","meaning":"n. 排放","example":"Factories must reduce harmful emissions.","exampleCn":"工厂必须减少有害排放。"},
    {"word":"pollutant","phonetic":"/pəˈluːtənt/","meaning":"n. 污染物","example":"Air pollutants affect respiratory health.","exampleCn":"空气污染物影响呼吸健康。"},
    {"word":"biodiversity","phonetic":"/ˌbaɪəʊdaɪˈvɜːsəti/","meaning":"n. 生物多样性","example":"Rainforests are rich in biodiversity.","exampleCn":"雨林拥有丰富的生物多样性。"},
    {"word":"ecosystem","phonetic":"/ˈiːkəʊsɪstəm/","meaning":"n. 生态系统","example":"Coral reefs are delicate ecosystems.","exampleCn":"珊瑚礁是脆弱的生态系统。"},
    {"word":"renewable","phonetic":"/rɪˈnjuːəbl/","meaning":"adj. 可再生的","example":"Solar power is a renewable energy source.","exampleCn":"太阳能是可再生能源。"},
    {"word":"deforestation","phonetic":"/ˌdiːfɒrɪˈsteɪʃn/","meaning":"n. 森林砍伐","example":"Deforestation accelerates climate change.","exampleCn":"森林砍伐加速气候变化。"},
    {"word":"habitat","phonetic":"/ˈhæbɪtæt/","meaning":"n. 栖息地","example":"Urban expansion destroys natural habitats.","exampleCn":"城市扩张破坏自然栖息地。"},
    {"word":"contaminate","phonetic":"/kənˈtæmɪneɪt/","meaning":"v. 污染","example":"Industrial waste can contaminate water sources.","exampleCn":"工业废物会污染水源。"},
    {"word":"extinction","phonetic":"/ɪkˈstɪŋkʃn/","meaning":"n. 灭绝","example":"Many species face the threat of extinction.","exampleCn":"许多物种面临灭绝威胁。"},
    {"word":"conservationist","phonetic":"/ˌkɒnsəˈveɪʃənɪst/","meaning":"n. 环保主义者","example":"Conservationists campaign for wildlife protection.","exampleCn":"环保主义者为野生动物保护而行动。"},
    {"word":"greenhouse effect","phonetic":"/ˈɡriːnhaʊs ɪˈfekt/","meaning":"n. 温室效应","example":"The greenhouse effect is causing global warming.","exampleCn":"温室效应导致全球变暖。"},
    {"word":"legislation","phonetic":"/ˌledʒɪsˈleɪʃn/","meaning":"n. 立法","example":"Environmental legislation has become more stringent.","exampleCn":"环境立法变得越来越严格。"},
    {"word":"biodegradable","phonetic":"/ˌbaɪəʊdɪˈɡreɪdəbl/","meaning":"adj. 可生物降解的","example":"Biodegradable packaging reduces plastic waste.","exampleCn":"可生物降解包装减少塑料废物。"},
    {"word":"ecological","phonetic":"/ˌiːkəˈlɒdʒɪkl/","meaning":"adj. 生态的","example":"Urban sprawl has major ecological impacts.","exampleCn":"城市扩张有重大生态影响。"},
    {"word":"fossil fuel","phonetic":"/ˈfɒsl ˈfjuːəl/","meaning":"n. 化石燃料","example":"Burning fossil fuels releases carbon dioxide.","exampleCn":"燃烧化石燃料释放二氧化碳。"},
    {"word":"global warming","phonetic":"/ˈɡləʊbl ˈwɔːmɪŋ/","meaning":"n. 全球变暖","example":"Global warming threatens coastal communities.","exampleCn":"全球变暖威胁沿海社区。"},
    {"word":"climate","phonetic":"/ˈklaɪmət/","meaning":"n. 气候","example":"Climate patterns are shifting dramatically.","exampleCn":"气候模式正在剧烈变化。"},
    {"word":"recycle","phonetic":"/ˌriːˈsaɪkl/","meaning":"v. 回收","example":"Households should recycle more diligently.","exampleCn":"家庭应更认真地回收。"},
    {"word":"toxic","phonetic":"/ˈtɒksɪk/","meaning":"adj. 有毒的","example":"Toxic chemicals must be disposed of safely.","exampleCn":"有毒化学品必须安全处理。"},
    {"word":"urbanization","phonetic":"/ˌɜːbənaɪˈzeɪʃn/","meaning":"n. 城市化","example":"Rapid urbanization strains natural resources.","exampleCn":"快速城市化给自然资源带来压力。"},
    {"word":"environmentalist","phonetic":"/ɪnˌvaɪrənˈmentəlɪst/","meaning":"n. 环保人士","example":"Environmentalists push for stronger climate policies.","exampleCn":"环保人士推动更强气候政策。"},
    {"word":"energy-efficient","phonetic":"/ˈenədʒi ɪˈfɪʃnt/","meaning":"adj. 节能的","example":"Energy-efficient homes reduce utility bills.","exampleCn":"节能房屋减少水电费。"},
    {"word":"reforestation","phonetic":"/ˌriːfɒrɪˈsteɪʃn/","meaning":"n. 重新造林","example":"Reforestation helps restore damaged land.","exampleCn":"重新造林有助于恢复受损土地。"},
    {"word":"atmosphere","phonetic":"/ˈætməsfɪər/","meaning":"n. 大气层","example":"Greenhouse gases trap heat in the atmosphere.","exampleCn":"温室气体在大气中捕获热量。"},
    {"word":"depletion","phonetic":"/dɪˈpliːʃn/","meaning":"n. 耗竭","example":"Ozone depletion is a serious concern.","exampleCn":"臭氧耗竭是一个严重问题。"},
    {"word":"waste management","phonetic":"/weɪst ˈmænɪdʒmənt/","meaning":"n. 废物管理","example":"Effective waste management is crucial for cities.","exampleCn":"有效的废物管理对城市至关重要。"},
    {"word":"marine","phonetic":"/məˈriːn/","meaning":"adj. 海洋的","example":"Marine life is threatened by plastic pollution.","exampleCn":"海洋生物受到塑料污染的威胁。"},
    {"word":"preservation","phonetic":"/ˌprezəˈveɪʃn/","meaning":"n. 保存，保护","example":"The preservation of wetlands is a priority.","exampleCn":"保护湿地是优先事项。"},
    {"word":"mitigate","phonetic":"/ˈmɪtɪɡeɪt/","meaning":"v. 减轻，缓解","example":"We must mitigate the effects of climate change.","exampleCn":"我们必须减轻气候变化的影响。"},
    {"word":"adaptation","phonetic":"/ˌædæpˈteɪʃn/","meaning":"n. 适应","example":"Climate adaptation plans are needed globally.","exampleCn":"全球需要气候适应计划。"},
    {"word":"overconsumption","phonetic":"/ˌəʊvəkənˈsʌmpʃn/","meaning":"n. 过度消费","example":"Overconsumption of resources is unsustainable.","exampleCn":"过度消费资源是不可持续的。"},
    {"word":"eco-friendly","phonetic":"/ˈiːkəʊ ˈfrendli/","meaning":"adj. 环保的","example":"Eco-friendly products are gaining market share.","exampleCn":"环保产品获得市场份额。"},
    {"word":"degradation","phonetic":"/ˌdeɡrəˈdeɪʃn/","meaning":"n. 退化","example":"Land degradation threatens food security.","exampleCn":"土地退化威胁粮食安全。"},
    {"word":"conservation area","phonetic":"/ˌkɒnsəˈveɪʃn ˈeəriə/","meaning":"n. 保护区","example":"National parks are vital conservation areas.","exampleCn":"国家公园是重要的保护区。"},
    {"word":"carbon footprint","phonetic":"/ˈkɑːbən ˈfʊtprɪnt/","meaning":"n. 碳足迹","example":"Everyone should try to reduce their carbon footprint.","exampleCn":"每个人都应努力减少碳足迹。"},
    {"word":"renewable energy","phonetic":"/rɪˈnjuːəbl ˈenədʒi/","meaning":"n. 可再生能源","example":"Investment in renewable energy is growing rapidly.","exampleCn":"可再生能源投资快速增长。"},
    {"word":"emission reduction","phonetic":"/ɪˈmɪʃn rɪˈdʌkʃn/","meaning":"n. 减排","example":"Countries set ambitious emission reduction targets.","exampleCn":"各国设定雄心勃勃的减排目标。"},
    {"word":"renewable resource","phonetic":"/rɪˈnjuːəbl rɪˈsɔːs/","meaning":"n. 可再生资源","example":"Water is a renewable resource but needs care.","exampleCn":"水是可再生资源但需要谨慎管理。"},
    {"word":"afforestation","phonetic":"/əˌfɒrɪˈsteɪʃn/","meaning":"n. 造林","example":"Afforestation programs help combat desertification.","exampleCn":"造林计划有助于防治荒漠化。"},
    {"word":"carbon neutral","phonetic":"/ˈkɑːbən ˈnjuːtrəl/","meaning":"adj. 碳中和的","example":"Many companies aim to become carbon neutral.","exampleCn":"许多公司目标是实现碳中和。"},
    {"word":"desertification","phonetic":"/dɪˌzɜːtɪfɪˈkeɪʃn/","meaning":"n. 荒漠化","example":"Desertification affects millions of hectares annually.","exampleCn":"荒漠化每年影响数百万公顷。"},
    {"word":"environmental degradation","phonetic":"/ɪnˌvaɪrənˈmentl ˌdeɡrəˈdeɪʃn/","meaning":"n. 环境退化","example":"Environmental degradation has accelerated in recent decades.","exampleCn":"环境退化在近几十年加速。"},
    {"word":"photosynthesis","phonetic":"/ˌfəʊtəʊˈsɪnθəsɪs/","meaning":"n. 光合作用","example":"Trees absorb CO2 through photosynthesis.","exampleCn":"树木通过光合作用吸收二氧化碳。"},
    {"word":"carbon sink","phonetic":"/ˈkɑːbən sɪŋk/","meaning":"n. 碳汇","example":"Forests act as important carbon sinks.","exampleCn":"森林充当重要的碳汇。"},
    {"word":"tectonic","phonetic":"/tekˈtɒnɪk/","meaning":"adj. 地壳构造的","example":"Tectonic activity shapes the Earth's surface.","exampleCn":"地壳构造活动塑造地球表面。"},
    {"word":"anthropogenic","phonetic":"/ˌænθrəpəˈdʒenɪk/","meaning":"adj. 人为的","example":"Anthropogenic emissions are the main cause of global warming.","exampleCn":"人为排放是全球变暖的主因。"},
    {"word":"conservationist","phonetic":"/ˌkɒnsəˈveɪʃənɪst/","meaning":"n. 环保人士","example":"Conservationists play a key role in policy advocacy.","exampleCn":"环保人士在政策倡导中发挥关键作用。"},
    {"word":"ecological footprint","phonetic":"/ˌiːkəˈlɒdʒɪkl ˈfʊtprɪnt/","meaning":"n. 生态足迹","example":"Reducing our ecological footprint is essential.","exampleCn":"减少我们的生态足迹至关重要。"},
    {"word":"endangered","phonetic":"/ɪnˈdeɪndʒəd/","meaning":"adj. 濒危的","example":"The panda is no longer classified as endangered.","exampleCn":"大熊猫不再被列为濒危物种。"},
    {"word":"greenwashing","phonetic":"/ˈɡriːnwɒʃɪŋ/","meaning":"n. 漂绿","example":"Consumers are increasingly skeptical of greenwashing.","exampleCn":"消费者对漂绿行为越来越警惕。"},
  ],
  "technology": [
    {"word":"innovation","phonetic":"/ˌɪnəˈveɪʃn/","meaning":"n. 创新","example":"Innovation drives economic growth.","exampleCn":"创新驱动经济增长。"},
    {"word":"digital","phonetic":"/ˈdɪdʒɪtl/","meaning":"adj. 数字的","example":"The digital age has transformed communication.","exampleCn":"数字时代改变了通信。"},
    {"word":"automation","phonetic":"/ˌɔːtəˈmeɪʃn/","meaning":"n. 自动化","example":"Automation is reshaping the manufacturing industry.","exampleCn":"自动化正在重塑制造业。"},
    {"word":"cybersecurity","phonetic":"/ˌsaɪbəsɪˈkjʊərəti/","meaning":"n. 网络安全","example":"Cybersecurity threats are evolving rapidly.","exampleCn":"网络安全威胁正在快速演变。"},
    {"word":"algorithm","phonetic":"/ˈælɡərɪðəm/","meaning":"n. 算法","example":"Algorithms determine what content we see online.","exampleCn":"算法决定我们在网上看到什么内容。"},
    {"word":"bandwidth","phonetic":"/ˈbændwɪdθ/","meaning":"n. 带宽","example":"High bandwidth enables smooth video streaming.","exampleCn":"高带宽支持流畅视频播放。"},
    {"word":"breakthrough","phonetic":"/ˈbreɪkθruː/","meaning":"n. 突破","example":"The discovery was a scientific breakthrough.","exampleCn":"这一发现是科学上的突破。"},
    {"word":"compatible","phonetic":"/kəmˈpætəbl/","meaning":"adj. 兼容的","example":"The software is compatible with all devices.","exampleCn":"该软件与所有设备兼容。"},
    {"word":"data mining","phonetic":"/ˈdeɪtə maɪnɪŋ/","meaning":"n. 数据挖掘","example":"Data mining reveals hidden consumer patterns.","exampleCn":"数据挖掘揭示隐藏的消费模式。"},
    {"word":"device","phonetic":"/dɪˈvaɪs/","meaning":"n. 设备","example":"Smart devices are connected via the internet.","exampleCn":"智能设备通过互联网连接。"},
    {"word":"disruptive","phonetic":"/dɪsˈrʌptɪv/","meaning":"adj. 颠覆性的","example":"Disruptive technologies can transform entire industries.","exampleCn":"颠覆性技术可以改变整个行业。"},
    {"word":"encryption","phonetic":"/ɪnˈkrɪpʃn/","meaning":"n. 加密","example":"End-to-end encryption ensures data privacy.","exampleCn":"端到端加密确保数据隐私。"},
    {"word":"infrastructure","phonetic":"/ˈɪnfrəstrʌktʃər/","meaning":"n. 基础设施","example":"Digital infrastructure is the backbone of modern economies.","exampleCn":"数字基础设施是现代经济的支柱。"},
    {"word":"interface","phonetic":"/ˈɪntəfeɪs/","meaning":"n. 界面，接口","example":"A clean interface improves user experience.","exampleCn":"干净的界面改善用户体验。"},
    {"word":"logistics","phonetic":"/ləˈdʒɪstɪks/","meaning":"n. 物流","example":"AI optimizes logistics and supply chains.","exampleCn":"AI优化物流和供应链。"},
    {"word":"network","phonetic":"/ˈnetwɜːk/","meaning":"n. 网络","example":"5G networks provide ultra-fast connectivity.","exampleCn":"5G网络提供超快连接。"},
    {"word":"optimize","phonetic":"/ˈɒptɪmaɪz/","meaning":"v. 优化","example":"Businesses use AI to optimize their operations.","exampleCn":"企业使用AI优化运营。"},
    {"word":"patent","phonetic":"/ˈpeɪtnt/","meaning":"n. 专利","example":"Tech companies register thousands of patents.","exampleCn":"科技公司注册数千项专利。"},
    {"word":"privacy","phonetic":"/ˈpraɪvəsi/","meaning":"n. 隐私","example":"Data privacy is a growing concern.","exampleCn":"数据隐私日益受到关注。"},
    {"word":"productivity","phonetic":"/ˌprɒdʌkˈtɪvəti/","meaning":"n. 生产力","example":"Technology boosts workplace productivity.","exampleCn":"技术提高工作效率。"},
    {"word":"regulate","phonetic":"/ˈreɡjuleɪt/","meaning":"v. 监管","example":"Governments regulate AI to ensure safety.","exampleCn":"政府监管AI以确保安全。"},
    {"word":"revolutionize","phonetic":"/ˌrevəˈluːʃənaɪz/","meaning":"v. 彻底变革","example":"The internet revolutionized global communication.","exampleCn":"互联网彻底变革了全球通信。"},
    {"word":"robotics","phonetic":"/rəʊˈbɒtɪks/","meaning":"n. 机器人技术","example":"Robotics is transforming healthcare.","exampleCn":"机器人技术正在改变医疗。"},
    {"word":"sophisticated","phonetic":"/səˈfɪstɪkeɪtɪd/","meaning":"adj. 复杂的，精密的","example":"Sophisticated AI powers modern applications.","exampleCn":"精密的AI驱动现代应用。"},
    {"word":"surveillance","phonetic":"/sɜːˈveɪləns/","meaning":"n. 监控","example":"Mass surveillance raises ethical concerns.","exampleCn":"大规模监控引发伦理担忧。"},
    {"word":"telecommunication","phonetic":"/ˌtelikəˌmjuːnɪˈkeɪʃn/","meaning":"n. 电信","example":"Telecommunications connect the global population.","exampleCn":"电信连接全球人口。"},
    {"word":"technological","phonetic":"/ˌteknəˈlɒdʒɪkl/","meaning":"adj. 技术的","example":"Technological progress accelerates every year.","exampleCn":"技术进步每年都在加速。"},
    {"word":"virtual","phonetic":"/ˈvɜːtʃuəl/","meaning":"adj. 虚拟的","example":"Virtual reality is changing entertainment.","exampleCn":"虚拟现实正在改变娱乐。"},
    {"word":"wearable","phonetic":"/ˈweərəbl/","meaning":"adj./n. 可穿戴的","example":"Wearable devices track health metrics.","exampleCn":"可穿戴设备追踪健康指标。"},
    {"word":"e-commerce","phonetic":"/ˈiː kɒmɜːs/","meaning":"n. 电子商务","example":"E-commerce has reshaped the retail sector.","exampleCn":"电子商务重塑了零售行业。"},
    {"word":"blockchain","phonetic":"/ˈblɒktʃeɪn/","meaning":"n. 区块链","example":"Blockchain enables secure peer-to-peer transactions.","exampleCn":"区块链实现安全的点对点交易。"},
    {"word":"big data","phonetic":"/bɪɡ ˈdeɪtə/","meaning":"n. 大数据","example":"Big data drives insights in healthcare.","exampleCn":"大数据驱动医疗洞察。"},
    {"word":"cloud computing","phonetic":"/klaʊd kəmˈpjuːtɪŋ/","meaning":"n. 云计算","example":"Cloud computing offers scalable storage solutions.","exampleCn":"云计算提供可扩展的存储方案。"},
    {"word":"machine learning","phonetic":"/məˈʃiːn ˈlɜːnɪŋ/","meaning":"n. 机器学习","example":"Machine learning improves with more data.","exampleCn":"机器学习随着更多数据而改进。"},
    {"word":"smartphone","phonetic":"/ˈsmɑːtfəʊn/","meaning":"n. 智能手机","example":"Smartphones have become indispensable.","exampleCn":"智能手机已成为必需品。"},
    {"word":"artificial intelligence","phonetic":"/ˌɑːtɪˈfɪʃl ɪnˈtelɪdʒəns/","meaning":"n. 人工智能","example":"AI is revolutionizing diagnosis in healthcare.","exampleCn":"AI正在革新医疗诊断。"},
    {"word":"nanotechnology","phonetic":"/ˌnænəʊtekˈnɒlədʒi/","meaning":"n. 纳米技术","example":"Nanotechnology has applications in medicine.","exampleCn":"纳米技术在医学中有应用。"},
    {"word":"cyberspace","phonetic":"/ˈsaɪbəspeɪs/","meaning":"n. 网络空间","example":"Cyberspace is the new frontier of commerce.","exampleCn":"网络空间是商业的新领域。"},
    {"word":"gadget","phonetic":"/ˈɡædʒɪt/","meaning":"n. 小工具","example":"New gadgets are released every month.","exampleCn":"每个月都有新设备发布。"},
    {"word":"cyber","phonetic":"/ˈsaɪbər/","meaning":"adj. 网络的","example":"Cyber attacks are becoming more frequent.","exampleCn":"网络攻击变得越来越频繁。"},
    {"word":"server","phonetic":"/ˈsɜːvər/","meaning":"n. 服务器","example":"Cloud servers store vast amounts of data.","exampleCn":"云服务器存储海量数据。"},
    {"word":"encryption","phonetic":"/ɪnˈkrɪpʃn/","meaning":"n. 加密","example":"Strong encryption protects sensitive information.","exampleCn":"强加密保护敏感信息。"},
    {"word":"open source","phonetic":"/ˈəʊpən sɔːs/","meaning":"adj./n. 开源","example":"Open source software encourages collaboration.","exampleCn":"开源软件鼓励协作。"},
    {"word":"agile","phonetic":"/ˈædʒaɪl/","meaning":"adj. 敏捷的","example":"Agile development enables rapid iteration.","exampleCn":"敏捷开发实现快速迭代。"},
    {"word":"bandwidth","phonetic":"/ˈbændwɪdθ/","meaning":"n. 带宽","example":"Insufficient bandwidth causes lag in video calls.","exampleCn":"带宽不足导致视频通话延迟。"},
    {"word":"scalable","phonetic":"/ˈskeɪləbl/","meaning":"adj. 可扩展的","example":"Cloud architecture makes applications highly scalable.","exampleCn":"云架构使应用高度可扩展。"},
    {"word":"autonomous","phonetic":"/ɔːˈtɒnəməs/","meaning":"adj. 自主的，自动的","example":"Autonomous vehicles are being tested worldwide.","exampleCn":"自动驾驶汽车正在全球测试。"},
    {"word":"quantum","phonetic":"/ˈkwɒntəm/","meaning":"adj./n. 量子","example":"Quantum computing promises exponential speedup.","exampleCn":"量子计算承诺指数级加速。"},
  ]
}

# ── Reading passage variants per theme (3 each) ──────────────────────────
READING = {
  "education": [
    {
      "title": "The Evolving Landscape of Education",
      "content": """Education has undergone significant transformation. A **comprehensive** education system now emphasizes not only **academic** knowledge but also **holistic** development. **Pedagogical** approaches have shifted from **rote** memorization toward **interactive** learning that **stimulates** critical thinking.

**Tertiary** institutions face pressure to update their **curriculum** to meet modern demands. The rising cost of **tuition** has sparked debate about educational **inequality**, with many calling for increased **scholarship** programs. **Vocational** training has gained recognition for providing practical **competence**.

Technology continues to **facilitate** learning through **innovative** tools. However, the **phenomenon** of digital distraction poses challenges. Effective educators **nurture** **motivation** and **dedicate** themselves to unlocking every student's **potential**. A **diverse** and inclusive approach remains the cornerstone of modern education."""
    },
    {
      "title": "Challenges and Opportunities in Modern Education",
      "content": """The modern education system faces both challenges and opportunities. One key issue is **discipline** in classrooms, which has become more complex as student populations become more **diverse**. Teachers must **nurture** an environment where all students can thrive while maintaining **rigorous** **academic** standards.

**Compulsory** education laws have improved **literacy** rates globally, but **illiterate** populations still exist. **Innovation** in **pedagogy** offers new ways to address these gaps. **Interactive** **seminars** and project-based learning **supplement** **conventional** lectures, **stimulating** deeper **cognitive** engagement.

Funding **allocation** remains contentious. Critics argue that educational **inequality** persists due to uneven resource distribution. **Vocational** programs need more support to provide practical **competence**. Ultimately, education must **facilitate** both personal growth and workforce readiness through a **comprehensive** approach."""
    },
    {
      "title": "Preparing Students for a Changing World",
      "content": """Education must evolve to prepare students for an uncertain future. Beyond **academic** knowledge, schools should **nurture** adaptability, creativity and emotional intelligence. The **curriculum** needs to balance **compulsory** subjects with flexible **specialization** options.

Assessment methods are being reimagined. Instead of relying solely on exams, many schools use continuous **assessment** to track progress. **Mentor** programs provide guidance, while **seminar**-based learning encourages deeper discussion. The **phenomenon** of lifelong learning reflects the understanding that education extends beyond formal schooling.

**Tertiary** institutions face challenges including rising **tuition** and **enrolment** pressures. **Scholarship** programs and government funding help address **inequality**. **Vocational** training offers alternative pathways. By combining **conventional** strengths with **innovative** approaches, education can **facilitate** both personal fulfillment and social progress."""
    }
  ],
  "environment": [
    {
      "title": "Our Planet at a Crossroads",
      "content": """The Earth faces unprecedented environmental challenges. **Anthropogenic** activities have accelerated **climate** change, with **emissions** from **fossil fuels** intensifying the **greenhouse effect**. **Global warming** is causing ice caps to melt and sea levels to rise.

**Conservation** efforts are critical to protect **biodiversity**. Natural **habitats** are being destroyed by **deforestation** and **urbanization**, pushing species toward **extinction**. **Marine** **ecosystems** suffer from plastic pollution and acidification.

Solutions exist but require commitment. Transitioning to **renewable energy** sources, improving **waste management**, and adopting **sustainable** practices can **mitigate** damage. **Reforestation** and **afforestation** restore **carbon sinks**. Strong **legislation** and individual action both play roles in environmental **preservation** for future generations."""
    },
    {
      "title": "The Path to Environmental Sustainability",
      "content": """Environmental **sustainability** requires urgent collective action. The **atmosphere** continues to warm as **greenhouse** gas concentrations rise. **Emission reduction** targets set by international agreements provide a framework, but progress remains insufficient.

**Ecological** damage from **overconsumption** and pollution threatens **biodiversity** worldwide. **Toxic** chemicals **contaminate** soil and water, while **plastic waste** chokes **marine** life. **Desertification** and land **degradation** reduce agricultural productivity.

Positive developments include the growth of **renewable energy**, **energy-efficient** technologies, and **eco-friendly** products. **Conservation areas** protect vulnerable species. **Environmentalist** movements raise awareness. Climate **adaptation** strategies help communities cope with changes already underway. The path forward requires both **mitigation** and **preservation** efforts at all levels of society."""
    },
    {
      "title": "Balancing Development and Environmental Protection",
      "content": """The tension between economic development and environmental **preservation** defines our era. **Urbanization** and industrial growth have improved living standards but at great **ecological** cost. **Deforestation** and **fossil fuel** consumption drive **global warming** and **habitat** loss.

**Conservation** strategies must evolve to address these challenges. **Carbon footprint** reduction requires changes in behavior and technology. **Renewable energy** and **energy-efficient** systems offer pathways to **sustainable** development. **Eco-friendly** innovations are becoming economically viable.

**Legislation** plays a crucial role. Government policies on **emission reduction**, **waste management**, and protected **conservation areas** create frameworks for action. Individual choices matter too — reducing **overconsumption**, recycling, and supporting **environmentalist** causes. The **adaptation** to a greener economy is not just necessary but possible through collective effort."""
    }
  ],
  "technology": [
    {
      "title": "How Technology is Reshaping Our World",
      "content": """Technology continues to **revolutionize** every aspect of modern life. **Digital** transformation has altered how we work, communicate, and access information. **Artificial intelligence** and **machine learning** algorithms analyze **big data** to generate insights that were previously impossible.

**Automation** and **robotics** are transforming industries from manufacturing to healthcare. While some fear job displacement, these technologies also boost **productivity** and create new opportunities. **Cloud computing** enables businesses to scale rapidly, while **blockchain** offers secure transaction platforms.

**Cybersecurity** has become critical as more activities move to **cyberspace**. **Encryption** protects **privacy**, but **surveillance** capabilities raise ethical questions. **Technological** breakthroughs in fields like **nanotechnology** promise solutions to major challenges. The key is to **regulate** these powerful tools wisely to maximize benefit while minimizing harm."""
    },
    {
      "title": "The Digital Revolution and Its Impacts",
      "content": """The **digital** revolution has fundamentally changed society. **Innovation** in **telecommunication** networks enables instant global connectivity. **Smartphones** and **wearable** devices have made technology personal and portable. **E-commerce** has transformed retail, while **virtual** experiences become increasingly immersive.

**Algorithm**-driven platforms shape what we see and buy. **Data mining** reveals consumer patterns but raises **privacy** concerns. **Cybersecurity** threats evolve alongside **sophisticated** defenses. The **infrastructure** supporting the **network** economy requires continuous investment.

**Disruptive** technologies like AI and **automation** are reshaping the job market. **Patents** protect **innovation**, but **open source** alternatives promote collaboration. **Regulate** efforts aim to balance progress with protection. **Technological** **literacy** has become as essential as traditional reading and writing skills in the modern workplace."""
    },
    {
      "title": "Innovation, Ethics, and the Future of Technology",
      "content": """As technology advances at an unprecedented pace, ethical considerations become increasingly important. **Artificial intelligence** systems make decisions that affect people's lives, raising questions about fairness and accountability. **Autonomous** vehicles and **robotics** challenge existing legal frameworks.

**Cybersecurity** and data **privacy** are fundamental rights in the **digital** age. **Encryption** protects individuals but can also shield illegal activity. **Surveillance** technologies offer security benefits but risk eroding civil liberties. **Biometric** data collection adds another layer of complexity.

The future promises **quantum** computing breakthroughs and further **automation**. **Nanotechnology** could revolutionize medicine. **Cloud computing** and **scalable** **infrastructure** will support growing demands. The challenge is to **innovate** responsibly — balancing **technological** progress with ethical considerations through thoughtful **regulation** and public dialogue."""
    }
  ]
}

# ── Reading question sets per theme (3 each) ───────────────────────────
QUESTIONS = {
  "education": [
    [
      {"question":"What has shifted in pedagogical approaches according to the passage?","options":["From interactive to rote learning","From rote memorization toward interactive learning","From vocational to academic training","From online to classroom learning"],"correct":1},
      {"question":"Why has tuition cost become a topic of debate?","options":["It has decreased significantly","It contributes to educational inequality","It only affects vocational schools","It is regulated by the government"],"correct":1},
      {"question":"What role does technology play in education?","options":["It replaces teachers entirely","It facilitates learning through innovative tools","It is only useful for vocational training","It reduces the need for curriculum"],"correct":1},
      {"question":"What does the passage say about a diverse educational approach?","options":["It is not necessary","It is the cornerstone of modern education","It only applies to tertiary education","It hinders academic progress"],"correct":1},
      {"question":"What do effective educators nurture in students?","options":["Only academic skills","Motivation and potential","Competition and grades","Discipline and obedience"],"correct":1},
    ],
    [
      {"question":"What has made classroom discipline more complex?","options":["Lack of funding","More diverse student populations","Online learning","Shorter school hours"],"correct":1},
      {"question":"What has improved global literacy rates?","options":["Online courses","Compulsory education laws","Private tutoring","International exams"],"correct":1},
      {"question":"How do interactive seminars supplement learning?","options":["They replace lectures entirely","They stimulate deeper cognitive engagement","They reduce the need for teachers","They focus only on exams"],"correct":1},
      {"question":"What persists despite efforts to improve education?","options":["High literacy rates","Educational inequality","Excessive funding","Too many teachers"],"correct":1},
      {"question":"What does education ultimately need to facilitate?","options":["Only workforce readiness","Only personal growth","Both personal growth and workforce readiness","Only academic excellence"],"correct":2},
    ],
    [
      {"question":"What should schools nurture beyond academic knowledge?","options":["Only discipline","Adaptability and emotional intelligence","Competition","Standardized test scores"],"correct":1},
      {"question":"How are assessment methods evolving?","options":["Only exams are used","Continuous assessment tracks progress","Assessment is no longer needed","Only final exams matter"],"correct":1},
      {"question":"What does the phenomenon of lifelong learning reflect?","options":["Education ends with formal schooling","Learning extends beyond formal schooling","Only adults need education","Formal education is unnecessary"],"correct":1},
      {"question":"What helps address educational inequality?","options":["Higher tuition fees","Scholarship programs and government funding","Reducing school years","Fewer teachers"],"correct":1},
      {"question":"What can education facilitate by combining old and new approaches?","options":["Only economic growth","Both personal fulfillment and social progress","Only academic achievement","Only career success"],"correct":1},
    ]
  ],
  "environment": [
    [
      {"question":"What has accelerated climate change according to the passage?","options":["Natural cycles","Anthropogenic activities","Solar radiation","Ocean currents"],"correct":0},
      {"question":"What is causing species to face extinction?","options":["Natural selection","Habitat destruction through deforestation and urbanization","Increased conservation efforts","Reduced pollution"],"correct":1},
      {"question":"What can mitigate environmental damage?","options":["Continuing current practices","Ignoring the problem","Sustainable practices and renewable energy","Increasing fossil fuel use"],"correct":2},
      {"question":"What restores carbon sinks?","options":["Urbanization","Deforestation","Reforestation and afforestation","Industrialization"],"correct":2},
      {"question":"What do both legislation and individual action contribute to?","options":["Economic growth","Environmental preservation","Technological progress","Urban development"],"correct":1},
    ],
    [
      {"question":"What provides a framework for emission reduction?","options":["Individual choices","International agreements","Corporate policies","Local ordinances"],"correct":1},
      {"question":"What threatens marine life?","options":["Overfishing only","Plastic pollution and acidification","Natural predators","Temperature increases only"],"correct":1},
      {"question":"What are positive environmental developments mentioned?","options":["Increased fossil fuel use","Growth of renewable energy and eco-friendly products","Reduced environmental regulations","More deforestation"],"correct":1},
      {"question":"What helps communities cope with climate changes?","options":["Ignoring the problem","Adaptation strategies","Increased emissions","Urban expansion"],"correct":1},
      {"question":"What is needed at all levels of society?","options":["More consumption","Mitigation and preservation efforts","Less regulation","Faster urbanization"],"correct":1},
    ],
    [
      {"question":"What defines the current era according to the passage?","options":["Technological progress","Tension between development and preservation","Global cooperation","Economic stability"],"correct":1},
      {"question":"What has driven global warming?","options":["Renewable energy","Deforestation and fossil fuel consumption","Conservation efforts","Reduced industrial activity"],"correct":1},
      {"question":"What offers pathways to sustainable development?","options":["Fossil fuels","Renewable energy and energy-efficient systems","Increased consumption","Deforestation"],"correct":1},
      {"question":"What creates frameworks for environmental action?","options":["Individual choices only","Corporate profits","Government legislation","International trade"],"correct":2},
      {"question":"What is possible through collective effort?","options":["Reversing all environmental damage","Eliminating pollution entirely","Adaptation to a greener economy","Stopping climate change immediately"],"correct":2},
    ]
  ],
  "technology": [
    [
      {"question":"What analyzes big data to generate insights?","options":["Human analysts","AI and machine learning algorithms","Traditional statistics","Manual processing"],"correct":1},
      {"question":"What is transforming industries from manufacturing to healthcare?","options":["Traditional methods","Automation and robotics","Manual labor","Government policies"],"correct":1},
      {"question":"What has become critical as more activities move to cyberspace?","options":["Bandwidth","Cybersecurity","Hardware","Electricity"],"correct":1},
      {"question":"What raises ethical questions according to the passage?","options":["Cloud computing","Surveillance capabilities","E-commerce","Smartphones"],"correct":1},
      {"question":"What is the key to managing powerful technologies?","options":["Banning them","Regulating them wisely","Ignoring them","Leaving them unregulated"],"correct":1},
    ],
    [
      {"question":"What enables instant global connectivity?","options":["Innovation in telecommunication","Traditional mail","Physical travel","Newspapers"],"correct":0},
      {"question":"What reveals consumer patterns but raises privacy concerns?","options":["Data mining","Manual surveys","Focus groups","Questionnaires"],"correct":0},
      {"question":"What is reshaping the job market?","options":["Traditional industries","Disruptive technologies and automation","Government regulations","Educational reforms"],"correct":1},
      {"question":"What promotes collaboration in technology?","options":["Patents","Open source alternatives","Corporate secrecy","Government control"],"correct":1},
      {"question":"What has become as essential as traditional literacy?","options":["Physical fitness","Technological literacy","Artistic ability","Musical talent"],"correct":1},
    ],
    [
      {"question":"What challenges existing legal frameworks?","options":["Traditional businesses","Autonomous vehicles and robotics","Manual processes","Simple machinery"],"correct":1},
      {"question":"What are fundamental rights in the digital age?","options":["Only freedom of speech","Cybersecurity and data privacy","Only property rights","Only voting rights"],"correct":1},
      {"question":"What adds complexity to privacy discussions?","options":["Biometric data collection","Traditional photography","Physical documents","Manual records"],"correct":0},
      {"question":"What could revolutionize medicine?","options":["Traditional surgery","Nanotechnology","Basic research","Conventional drugs"],"correct":1},
      {"question":"How should technological progress be balanced?","options":["Through restriction only","Through thoughtful regulation","Through complete freedom","Through international bans"],"correct":1},
    ]
  ]
}

# ── Writing variants per theme (3 each) ────────────────────────────────
WRITING = {
  "education": [
    {
      "type":"Discuss both views","task":"Task 2","time":"40 minutes",
      "prompt":"Some people believe that the primary purpose of education is to prepare individuals for the workforce. Others argue that education has a broader role in developing well-rounded individuals. Discuss both views and give your opinion.",
      "tips":["Start with a clear introduction","Dedicate one paragraph to each view","Use specific examples","Include vocabulary from today's list","Conclude with your personal opinion"],
      "suggestedVocab":["vocational","competence","comprehensive","nurture","cognitive","potential"]
    },
    {
      "type":"Agree or Disagree","task":"Task 2","time":"40 minutes",
      "prompt":"Some people think that all children should be required to learn a foreign language from primary school. Others believe this puts unnecessary pressure on young students. To what extent do you agree or disagree?",
      "tips":["State your position clearly","Consider both benefits and drawbacks","Provide evidence from research","Use academic vocabulary","Summarize your argument in conclusion"],
      "suggestedVocab":["compulsory","curriculum","cognitive","facilitate","motivation","rigorous"]
    },
    {
      "type":"Advantages and Disadvantages","task":"Task 2","time":"40 minutes",
      "prompt":"With the rise of online education, more students are choosing to study remotely rather than attending traditional classrooms. What are the advantages and disadvantages of this trend? Do the benefits outweigh the drawbacks?",
      "tips":["Structure your essay clearly","Discuss both sides equally","Use specific examples","Include topic-specific vocabulary","End with a balanced conclusion"],
      "suggestedVocab":["interactive","supplement","conventional","innovation","access","flexibility"]
    }
  ],
  "environment": [
    {
      "type":"Agree or Disagree","task":"Task 2","time":"40 minutes",
      "prompt":"Some people believe that environmental problems are too big for individuals to solve, and that only governments and large companies can make a real difference. To what extent do you agree or disagree?",
      "tips":["State your position clearly","Acknowledge the opposing view","Provide examples of both individual and government action","Use relevant vocabulary","Reinforce your overall argument"],
      "suggestedVocab":["sustainable","emission","conservation","legislation","mitigate","eco-friendly"]
    },
    {
      "type":"Discuss both views","task":"Task 2","time":"40 minutes",
      "prompt":"Economic growth is often prioritized over environmental protection in developing countries. Some argue that countries must develop first before they can afford to go green. Others say environmental protection cannot wait. Discuss both views.",
      "tips":["Define key terms in introduction","Present economic arguments first","Then present environmental arguments","Use specific country examples","Offer a balanced conclusion"],
      "suggestedVocab":["urbanization","ecological","degradation","renewable","adaptation","preservation"]
    },
    {
      "type":"Problems and Solutions","task":"Task 2","time":"40 minutes",
      "prompt":"Plastic pollution has become one of the most pressing environmental issues of our time. What problems does plastic pollution cause, and what measures can be taken to address this issue?",
      "tips":["Identify 2-3 key problems","Propose realistic solutions","Use specific data where relevant","Connect to broader environmental issues","Conclude with a call to action"],
      "suggestedVocab":["marine","toxic","biodegradable","waste management","eco-friendly","legislation"]
    }
  ],
  "technology": [
    {
      "type":"Agree or Disagree","task":"Task 2","time":"40 minutes",
      "prompt":"Some people believe that technological advancements have made our lives more complicated rather than simpler. To what extent do you agree or disagree with this statement?",
      "tips":["Start with a clear thesis","Acknowledge both benefits and drawbacks","Use examples from daily life","Include relevant vocabulary","Conclude with a balanced judgment"],
      "suggestedVocab":["innovation","digital","automation","productivity","sophisticated","revolutionize"]
    },
    {
      "type":"Discuss both views","task":"Task 2","time":"40 minutes",
      "prompt":"Social media has become an integral part of modern life. Some argue that it brings people closer together, while others believe it damages real-world relationships. Discuss both views and give your opinion.",
      "tips":["Introduce both perspectives","Provide specific examples of connection","Also highlight negative impacts","Use technology-specific vocabulary","Give a reasoned conclusion"],
      "suggestedVocab":["algorithm","privacy","network","cyberspace","interface","digital"]
    },
    {
      "type":"Positive or Negative","task":"Task 2","time":"40 minutes",
      "prompt":"Artificial intelligence is increasingly being used to make important decisions in areas such as healthcare, finance, and criminal justice. Is this a positive or negative development? Give reasons for your answer.",
      "tips":["Define AI clearly in introduction","Discuss benefits in specific fields","Address risks and concerns","Consider ethical implications","Provide a nuanced conclusion"],
      "suggestedVocab":["artificial intelligence","algorithm","regulate","sophisticated","breakthrough","cybersecurity"]
    }
  ]
}

# ── Speaking variants per theme (3 each) ───────────────────────────────
SPEAKING = {
  "education": [
    {
      "part1": [
        {"question":"Do you think education is important in your country? Why?","reference":"Education plays a vital role in shaping individuals and society. In my country, it is highly valued as a means to secure better career opportunities and personal growth."},
        {"question":"What subject did you enjoy most at school?","reference":"I was particularly fond of literature because it stimulated my imagination and helped me understand different perspectives."},
        {"question":"Do you think the education system in your country needs improvement?","reference":"While the system has its strengths, I believe there is room for improvement in terms of fostering creativity rather than focusing solely on exam results."}
      ],
      "part2": {"prompt":"Describe a teacher who made a significant impact on your life.\n- Who this teacher was\n- What subject they taught\n- How they influenced you\n- And explain why you remember them so vividly","reference":"I'd like to talk about my high school English teacher who transformed my attitude toward learning. She had a unique ability to make every lesson engaging and would often stay after class to provide extra guidance. Her mentorship had a profound impact on my academic journey."},
      "part3": [
        {"question":"How has education changed in your country over the past few decades?","reference":"Education has undergone significant transformation from traditional rote learning toward interactive and student-centered approaches. Technology has also played a crucial role in facilitating access to educational resources."},
        {"question":"What role should the government play in education?","reference":"The government should ensure equal access to quality education, allocate adequate funding, and establish rigorous standards while allowing room for innovation."},
        {"question":"Do you think online education will replace traditional classrooms?","reference":"While online education offers flexibility, I don't believe it will completely replace traditional classrooms. The interactive and social aspects of in-person learning are invaluable."}
      ]
    },
    {
      "part1": [
        {"question":"What is the most important skill students should learn at school?","reference":"I believe critical thinking is the most important skill because it enables students to analyze information independently and make informed decisions throughout their lives."},
        {"question":"Should students be allowed to choose what they study?","reference":"To some extent, yes. While a core curriculum ensures foundational knowledge, allowing students to specialize in areas of interest can boost motivation and engagement."},
        {"question":"Do you think exams are the best way to assess students?","reference":"Exams have their limitations. I think a combination of continuous assessment, projects, and exams provides a more comprehensive picture of a student's abilities."}
      ],
      "part2": {"prompt":"Describe a book that had a significant impact on your education.\n- What the book was\n- When you read it\n- What it taught you\n- And explain why it was important for your learning","reference":"I'd like to talk about 'Thinking, Fast and Slow' by Daniel Kahneman, which I read during my second year of university. It fundamentally changed how I understand decision-making and cognitive biases. The book taught me to question my assumptions and think more critically."},
      "part3": [
        {"question":"Should university education be free for all students?","reference":"While free education would promote equality, it poses significant funding challenges. A compromise could be means-tested tuition fees or expanded scholarship programs."},
        {"question":"How can technology improve the learning experience?","reference":"Technology can personalize learning paths, provide instant feedback, and make education more accessible. However, it should supplement rather than replace human teachers."},
        {"question":"What is the value of studying humanities in a technology-driven world?","reference":"Humanities develop critical thinking, empathy, and communication skills that are essential regardless of one's career. They help us understand the human condition and ethical implications of technological progress."}
      ]
    },
    {
      "part1": [
        {"question":"Do you prefer studying alone or in a group?","reference":"I prefer a mix of both. Studying alone helps me focus and organize my thoughts, while group study allows me to discuss ideas and learn from others' perspectives."},
        {"question":"What was your favorite subject when you were younger?","reference":"My favorite subject was history because I enjoyed learning about different cultures and understanding how past events shaped the present world."},
        {"question":"Do you think homework is necessary for learning?","reference":"Homework can reinforce what was taught in class, but too much can be counterproductive. Quality matters more than quantity when it comes to homework assignments."}
      ],
      "part2": {"prompt":"Describe a skill you learned outside of school that has been useful.\n- What the skill was\n- How you learned it\n- Why you decided to learn it\n- And explain how it has been useful","reference":"I taught myself basic programming through online courses during my summer break. I decided to learn it because I realized digital literacy was becoming essential in every field. This skill has been incredibly useful, helping me automate tasks and analyze data more effectively."},
      "part3": [
        {"question":"How can schools better prepare students for the future?","recommendation":"Schools should focus more on teaching adaptability, problem-solving, and digital skills rather than just memorization. Collaboration with industries could provide practical exposure."},
        {"question":"What is the role of early childhood education?","reference":"Early childhood education lays the foundation for cognitive and social development. Quality preschool programs can have lasting positive effects on a child's academic trajectory."},
        {"question":"Should character education be part of the school curriculum?","reference":"Character education, including values like honesty, responsibility, and empathy, is essential for developing well-rounded individuals who can contribute positively to society."}
      ]
    }
  ],
  "environment": [
    {
      "part1": [
        {"question":"Do you think environmental issues are important? Why?","reference":"Absolutely, environmental issues are crucial because they directly affect our quality of life and the future of our planet."},
        {"question":"What do you do to protect the environment?","reference":"I try to reduce my carbon footprint by using public transportation, recycling waste, and choosing eco-friendly products whenever possible."},
        {"question":"Is the environment better now than it was in the past?","reference":"In some ways it has improved due to greater awareness and stricter legislation, but challenges like global warming have become more severe."}
      ],
      "part2": {"prompt":"Describe a natural place you have visited that you found beautiful.\n- Where it was\n- When you visited it\n- What you saw there\n- And explain why you found it so beautiful","reference":"I'd like to talk about a visit to Jiuzhaigou Valley in Sichuan. The landscape was breathtaking with crystal-clear lakes surrounded by colorful forests and snow-capped mountains. The incredible biodiversity made me realize how important conservation efforts are."},
      "part3": [
        {"question":"Should economic development be prioritized over environmental protection?","reference":"I believe the two need not be mutually exclusive. Sustainable development aims to balance economic growth with environmental preservation."},
        {"question":"What can governments do to encourage people to be more environmentally friendly?","reference":"Governments can introduce legislation such as carbon taxes, provide subsidies for renewable energy, invest in public transportation, and launch awareness campaigns."},
        {"question":"How will climate change affect our daily lives?","reference":"Climate change will affect food production through changing weather patterns, increase the frequency of natural disasters, and potentially lead to migration from affected areas."}
      ]
    },
    {
      "part1": [
        {"question":"What environmental problem concerns you the most?","reference":"Plastic pollution concerns me greatly because it affects marine life and enters our food chain through microplastics."},
        {"question":"Should plastic bags be banned completely?","reference":"I think banning single-use plastic bags is a step in the right direction, but it should be accompanied by affordable alternatives and public education."},
        {"question":"Do you think young people are more environmentally aware than older generations?","reference":"Young people tend to be more aware because environmental education has become more prominent in schools, and they are more exposed to environmental content on social media."}
      ],
      "part2": {"prompt":"Describe something you do to help the environment.\n- What you do\n- How often you do it\n- Why you started doing it\n- And explain how this helps the environment","reference":"I make a conscious effort to reduce food waste by planning meals weekly, composting scraps, and storing food properly. I started doing this after learning that food waste in landfills produces methane. It helps reduce greenhouse gas emissions and saves money."},
      "part3": [
        {"question":"Can technology solve environmental problems?","reference":"Technology can provide powerful solutions like renewable energy and carbon capture, but it is not a silver bullet. Behavioral change and policy reforms are equally important."},
        {"question":"How can individuals make a meaningful impact on the environment?","reference":"Individual actions collectively make a significant difference. Reducing consumption, choosing sustainable products, and voting for environmental policies all contribute."},
        {"question":"What is the biggest obstacle to environmental progress?","reference":"The biggest obstacle is probably short-term thinking — prioritizing immediate economic gains over long-term sustainability. Overcoming this requires both education and policy changes."}
      ]
    },
    {
      "part1": [
        {"question":"Have you ever participated in any environmental activities?","reference":"Yes, I've joined community beach clean-ups and tree-planting events. These activities are not only helpful but also raise awareness among participants."},
        {"question":"What is your opinion on electric vehicles?","reference":"I think electric vehicles are a positive development, especially when charged using renewable energy. However, battery production and disposal still pose environmental challenges."},
        {"question":"Do you think climate change is exaggerated by the media?","reference":"I believe the media sometimes sensationalizes climate stories, but the underlying scientific consensus is clear — climate change is real and requires urgent action."}
      ],
      "part2": {"prompt":"Describe a change you have made to live more sustainably.\n- What the change was\n- When you made it\n- Was it difficult to implement\n- And explain how it has affected your life","reference":"I decided to become a vegetarian about two years ago after learning about the environmental impact of meat production. It was challenging at first, but I gradually discovered delicious plant-based alternatives. This change has not only reduced my ecological footprint but also improved my health."},
      "part3": [
        {"question":"What role should international organizations play in environmental protection?","reference":"International organizations can facilitate global cooperation, set emission reduction targets, provide funding for green projects in developing countries, and monitor progress."},
        {"question":"How does consumer behavior affect the environment?","reference":"Consumer behavior drives production. When people choose sustainable products, companies respond by offering greener options. Conversely, overconsumption of fast fashion and single-use items harms the environment."},
        {"question":"What are the environmental consequences of urbanization?","reference":"Urbanization leads to habitat loss, increased emissions, higher energy consumption, and waste management challenges. However, well-planned cities can actually be more environmentally efficient than suburban sprawl."}
      ]
    }
  ],
  "technology": [
    {
      "part1": [
        {"question":"How often do you use technology in your daily life?","reference":"I use technology constantly throughout the day, from my smartphone alarm to streaming services. It has become an integral part of my routine."},
        {"question":"What is your favorite piece of technology?","reference":"My smartphone is my favorite because it combines communication, information access, entertainment, and productivity all in one device."},
        {"question":"Do you think technology makes people lazy?","reference":"While technology automates many tasks, I believe it frees up mental energy for more creative and meaningful work rather than making people lazy."}
      ],
      "part2": {"prompt":"Describe a piece of technology that has changed your life.\n- What it is\n- When you started using it\n- How it changed your daily routine\n- And explain why you think it's important","reference":"My smartphone has completely transformed how I live and work. I got my first one about ten years ago, and since then it has revolutionized my daily routine. It has made information instantly accessible and connected me with people across the globe."},
      "part3": [
        {"question":"Will AI replace human workers in the future?","reference":"While AI will automate certain jobs, it will also create new roles. The key is for workers to adapt and develop skills that complement AI rather than compete with it."},
        {"question":"How has social media changed communication?","reference":"Social media has made communication instant and global, but it has also raised concerns about privacy, misinformation, and the quality of interpersonal relationships."},
        {"question":"What role should government play in regulating technology?","reference":"Governments should balance encouraging innovation and protecting citizens through regulation of data privacy, cybersecurity, and AI ethics."}
      ]
    },
    {
      "part1": [
        {"question":"How do you think technology will change in the next ten years?","reference":"I expect AI to become even more integrated into daily life, with advances in autonomous vehicles, personalized medicine, and smart cities."},
        {"question":"Do you think children spend too much time on screens?","reference":"I think screen time needs to be balanced with physical activity and face-to-face interaction. Technology can be educational, but moderation is important."},
        {"question":"What technology could you not live without?","reference":"I could not live without internet access because it is essential for my work, communication, and access to information."}
      ],
      "part2": {"prompt":"Describe a time when technology helped you solve a problem.\n- What the problem was\n- What technology you used\n- How it helped\n- And explain why it was effective","reference":"When I was planning a trip abroad, I used a combination of translation apps, maps, and travel planning tools to navigate a country where I didn't speak the language. These technologies made the entire experience smooth and enjoyable."},
      "part3": [
        {"question":"Is technology making society more unequal?","reference":"There is a digital divide — those without access to technology or digital skills are at a disadvantage. Bridging this gap should be a priority for governments."},
        {"question":"How is technology changing the healthcare industry?","reference":"Technology is revolutionizing healthcare through AI diagnosis, telemedicine, wearable health monitors, and personalized treatment based on genetic data."},
        {"question":"Should there be limits on technological development?","reference":"Rather than limits, I think there should be ethical guidelines and oversight. Technologies like AI and genetic engineering need careful regulation without stifling innovation."}
      ]
    },
    {
      "part1": [
        {"question":"Do you prefer reading physical books or e-books?","reference":"I prefer physical books for deep reading because I find it easier to concentrate without digital distractions, but e-books are convenient for travel."},
        {"question":"How has technology changed the way people work?","reference":"Technology has enabled remote work, flexible hours, and global collaboration. However, it has also blurred the boundary between work and personal life."},
        {"question":"Are you concerned about data privacy online?","reference":"Yes, I am concerned. Companies collect vast amounts of personal data, and I worry about how this information is used and protected from breaches."}
      ],
      "part2": {"prompt":"Describe an app or software that you find very useful.\n- What it is\n- What it does\n- How you use it\n- And explain why you find it so useful","reference":"I find Notion incredibly useful for organizing my work and personal life. It combines note-taking, task management, and database functions in one platform. I use it to plan projects, track goals, and store reference materials."},
      "part3": [
        {"question":"How is artificial intelligence changing education?","reference":"AI enables personalized learning experiences, adapts to individual student needs, and provides instant feedback. However, it cannot replace the mentorship and emotional support of human teachers."},
        {"question":"What are the ethical concerns surrounding facial recognition technology?","reference":"Facial recognition raises concerns about privacy, consent, and potential bias. There are also fears about mass surveillance and the erosion of anonymity in public spaces."},
        {"question":"Will technology make traditional schools obsolete?","reference":"I doubt it. While technology enhances learning, schools provide social interaction, structure, and guidance that are difficult to replicate digitally."}
      ]
    }
  ]
}


def pick_variant(seed, n_variants):
    """Deterministically pick a variant index based on date seed."""
    rng = random.Random(seed)
    return rng.randint(0, n_variants - 1)


def generate_today_content():
    today = __import__('datetime').date.today().isoformat()
    seed = today  # Use date string as seed for deterministic selection

    # Read existing themes.json to preserve theme list
    themes_path = os.path.join(BASE, 'content', 'themes.json')
    with open(themes_path, 'r', encoding='utf-8') as f:
        themes_data = json.load(f)

    for theme in themes_data['themes']:
        tid = theme['id']
        word_pool = WORDS[tid]
        n_variants = len(QUESTIONS[tid])

        variant = pick_variant(seed + tid, n_variants)

        # Pick 40 words using a deterministic subset
        rng = random.Random(seed + tid)
        selected_words = rng.sample(word_pool, min(40, len(word_pool)))

        reading = READING[tid][variant]
        questions = QUESTIONS[tid][variant]
        writing = WRITING[tid][variant]
        speaking = SPEAKING[tid][variant]

        data = {
            "words": selected_words,
            "reading": reading,
            "readingQuestions": questions,
            "writing": writing,
            "speaking": {
                "part1": speaking["part1"],
                "part2": speaking["part2"],
                "part3": speaking["part3"]
            }
        }

        theme_dir = os.path.join(BASE, 'content', tid)
        os.makedirs(theme_dir, exist_ok=True)
        data_path = os.path.join(theme_dir, 'data.json')
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {tid} (variant {variant + 1}/{n_variants}, {len(selected_words)} words)")

    themes_data['lastUpdated'] = today
    with open(themes_path, 'w', encoding='utf-8') as f:
        json.dump(themes_data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ themes.json updated to {today}")


if __name__ == '__main__':
    print(f"Generating IELTS content for {__import__('datetime').date.today().isoformat()}...")
    generate_today_content()
    print("Done!")
