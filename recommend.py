import math
#读取文件，records存储标签数据的三元组，records[i] = [user, item, tag]
def ReadTags():
    data_file = open('tags.txt','r')
    next(data_file)
    records = data_file.readlines()
    data_file.close()
    return records

def addValueToMat(mat, key, value):
    if key not in mat:
        mat[key] = dict()
        mat[key][value] = 1
    else:
        if value not in mat[key]:
            mat[key][value] = 1
        else:
            mat[key][value] += 1

user_tags = dict()
tag_items = dict()
user_items = dict()
item_tags = dict()
def InitStat(records):
    for record in records:
        record = record.split("\t")
        user = record[0]
        item = record[1]
        tag = record[2]
        addValueToMat(user_tags, user, tag)
        addValueToMat(tag_items, tag, item)
        addValueToMat(user_items, user, item)
        addValueToMat(item_tags, item, tag)

#计算推荐列表
def Recommend(user):
    recommend_items = dict()
    tagged_items = user_items[user]
    for tag, wut in user_tags[user].items():
        for item, wti in tag_items[tag].items():
            if item in tagged_items:
                continue
            if item not in recommend_items:
                recommend_items[item] = wut * wti
            else:
                recommend_list[item] += wut * wti
    return sorted(recommend_items.items(), key = lambda a:a[1], reverse = True)

#计算标签流行度
def TagPopularity():
    tagfreq = {}
    for user in user_tags.keys():
        for tag in user_tags[user].keys():
            if tag not in tagfreq:
                tagfreq[tag] = 1
            else:
                tagfreq[tag] += 1
    return sorted(tagfreq.items(), key = lambda a:a[1], reverse = True)

#计算余弦相似度
def CosineSim(item_tags, i, j):
    ret = 0
    for b, wib in item_tags[i].items():     #求物品i,j的标签交集数目
        if b in item_tags[j]:
            ret += wib * item_tags[j][b]
    ni = 0
    nj = 0
    for b, w in item_tags[i].items():      #统计 i 的标签数目
        ni += w * w
    for b, w in item_tags[j].items():      #统计 j 的标签数目
        nj += w * w
    if ret == 0:
        return 0
    return ret / math.sqrt(ni * nj)

#计算多样性
def Diversity(item_tags, recommend_items):
    ret = 0
    n = 0
    for i in dict(recommend_items).keys():
        for j in dict(recommend_items).keys():
            if i == j:
                continue
            ret += CosineSim(item_tags, i ,j)
            n += 1
    return ret / (n * 1.0)

records = ReadTags()
InitStat(records)
recommend_items = Recommend('2')
tagfreq = TagPopularity()
print("Recommend List: %s" %recommend_items)
print("Tag Popularity: %s" %tagfreq)
diversity = Diversity(item_tags, recommend_items)
print("Diversity: %s" %diversity)
