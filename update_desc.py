import requests
import os

# 配置项
API_URL = "https://api.niany.cn/v2/today_in_history"
FILE_PATH = "main.xaml"
# 兜底内容（API失败时使用）
DEFAULT_HISTORY_CONTENT = '''<local:MyCard Title="暂无历史数据" Margin="0,0,0,15" CanSwap="False" IsSwaped="True">
    <StackPanel Margin="25,40,23,15">
        <TextBlock TextWrapping="Wrap" Margin="0,0,0,4" Text="暂时无法获取历史上的今天数据，请去疯狂@作者。" />
    </StackPanel>
</local:MyCard>'''


WELCOME_CONTENT = '''<local:MyCard Margin="0,-6,0,12" Title="欢迎 勿忘历史，牢记使命"> <!--下面不是卡片，所以不用0,0,0,12-->
     <StackPanel Margin="24,35,24,15">
          <TextBlock HorizontalAlignment="Center" Margin="0,0,0,0"
               Foreground="{DynamicResource ColorBrush2}" FontSize="20"
               Text="欢迎使用历史上的今天主页!" />
          <Calendar HorizontalAlignment="Center" Margin="0,12,0,10" />
          <TextBlock Margin="5,0,5,12" TextWrapping="Wrap" HorizontalAlignment="Center"
               Foreground="{DynamicResource ColorBrush1}" Text="{cave}" />
     </StackPanel>
</local:MyCard> 

'''


FIXED_CONTENT = '''<local:MyCard Margin="0,0,0,8">
     <StackPanel Margin="24,6,24,12">
          <Grid>
               <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="1*" />
                    <ColumnDefinition Width="1*" />
               </Grid.ColumnDefinitions>
               <local:MyIconTextButton Margin="0,5,0,6" Height="35" HorizontalAlignment="Center"
                    Text="作者网站" EventType="打开网页" Grid.Column="0"
                    EventData="https://llsgllsg.rth1.xyz"
                    LogoScale="0.8" ColorType="Highlight"
                    Logo="M13.5,4A1.5,1.5 0 0,0 12,5.5A1.5,1.5 0 0,0 13.5,7A1.5,1.5 0 0,0 15,5.5A1.5,1.5 0 0,0 13.5,4M13.14,8.77C11.95,8.87 8.7,11.46 8.7,11.46C8.5,11.61 8.56,11.6 8.72,11.88C8.88,12.15 8.86,12.17 9.05,12.04C9.25,11.91 9.58,11.7 10.13,11.36C12.25,10 10.47,13.14 9.56,18.43C9.2,21.05 11.56,19.7 12.17,19.3C12.77,18.91 14.38,17.8 14.54,17.69C14.76,17.54 14.6,17.42 14.43,17.17C14.31,17 14.19,17.12 14.19,17.12C13.54,17.55 12.35,18.45 12.19,17.88C12,17.31 13.22,13.4 13.89,10.71C14,10.07 14.3,8.67 13.14,8.77Z" />
               <local:MyIconTextButton Margin="0,5,0,6" Height="35" HorizontalAlignment="Center"
                    Text="刷新主页" EventType="刷新主页" Grid.Column="1"
                    LogoScale="0.8" ColorType="Highlight"
                    Logo="M256.455,8C322.724,8.119,382.892,34.233,427.314,76.685L463.029,40.97C478.149,25.851,504,36.559,504,57.941L504,192C504,205.255,493.255,216,480,216L345.941,216C324.559,216,313.851,190.149,328.97,175.029L370.72,133.279C339.856,104.38 299.919,88.372 257.49,88.006 165.092,87.208 87.207,161.983 88.0059999999999,257.448 88.764,348.009 162.184,424 256,424 297.127,424 335.997,409.322 366.629,382.444 371.372,378.283 378.535,378.536 382.997,382.997L422.659,422.659C427.531,427.531 427.29,435.474 422.177,440.092 378.202,479.813 319.926,504 256,504 119.034,504 8.001,392.967 8,256.002 7.999,119.193 119.646,7.755 256.455,8z" />
          </Grid>
          <local:MyListItem Margin="-2,0,0,0"
               Logo="pack://application:,,,/images/blocks/GoldBlock.png" Title="今日人品"
               Info="试试手气！" EventType="今日人品" Type="Clickable" />
          <local:MyListItem Margin="-2,0,0,0"
               Logo="pack://application:,,,/images/blocks/Grass.png" Title="启动基岩版"
               Info="以 URL Scheme 的方式启动电脑上的 MC 基岩版。" EventType="打开网页" EventData="minecraft://"
               Type="Clickable" />
          <local:MyListItem Margin="-2,0,0,0"
               Logo="pack://application:,,,/images/blocks/CommandBlock.png" Title="网页捷径"
               Type="Clickable"
               Info="打开网页捷径页面" EventType="打开帮助"
               EventData="https://mfn233.github.io/PCL-Mainpage/urlshortcut/main.json" />
<!--十分感谢MFn233的简单主页的部分代码此主页使用了MFn233简单主页的代码更新历史事件使用了一个不知名API和github actions自动部署-->
<local:MyListItem Margin="-2,0,0,0" Info="llsgllsg"
 Logo="pack://application:,,,/images/Blocks/Fabric.png" Title="关于作者"
EventType="弹出窗口"
 EventData="关于作者|我是llsgllsg，啥都会一丢丢的学生，该主页部分使用了MFn233的代码，并在GitHub上开源。欢迎你前往仓库为我的项目提issue
©llsgllsg 2026"
 Type="Clickable" />
</StackPanel>
</local:MyCard>

'''

def main():
    history_content = DEFAULT_HISTORY_CONTENT
    
    try:
        print("=== 开始请求API ===")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(API_URL, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            history_items = data.get("data", {}).get("items", [])
            
            if history_items:
                # 构建历史事件卡片
                history_cards = []
                for item in history_items:
                    title = item.get("title", "无标题")
                    year = item.get("year", "未知年份")
                    event_type = item.get("event_type", "未知类型")
                    desc_text = item.get("description", "无描述")
                    
                    card = f'''<local:MyCard Title="{year}年 - {title}（类型：{event_type}）" Margin="0,0,0,15" CanSwap="False" IsSwaped="True">
    <StackPanel Margin="25,40,23,15">
        <TextBlock TextWrapping="Wrap" Margin="0,0,0,4" Text="{desc_text}" />
    </StackPanel>
</local:MyCard>'''
                    history_cards.append(card)
                history_content = "\n\n".join(history_cards)
                print(f"✅ API请求成功，获取到 {len(history_items)} 条历史事件")
            else:
                print("⚠️ API返回空的历史事件列表，使用兜底内容")
        else:
            print(f"⚠️ API请求失败（状态码：{response.status_code}），使用兜底内容")
    except Exception as e:
        print(f"⚠️ API请求出错：{str(e)}，使用兜底内容")
    
    full_content = WELCOME_CONTENT + history_content + "\n\n" + FIXED_CONTENT
    
    try:
        abs_file_path = os.path.abspath(FILE_PATH)
        print(f"\n=== 开始写入文件：{abs_file_path} ===")
        
        with open(FILE_PATH, "w", encoding='utf-8') as f:
            f.write(full_content)
        
        if os.path.exists(FILE_PATH):
            file_size = os.path.getsize(FILE_PATH)
            print(f"✅ 文件生成成功！文件大小：{file_size} 字节")
            print(f"文件位置：{abs_file_path}")
            print("✅ 内容顺序：欢迎卡片（最顶部）→ 历史事件 → 功能按钮/版权信息")
        else:
            print("❌ 文件生成失败！")
    except Exception as e:
        print(f"❌ 写入文件出错：{str(e)}")

if __name__ == "__main__":
    main()


