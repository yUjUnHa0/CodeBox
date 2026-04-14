"""
Flask主应用文件
功能：处理所有HTTP请求，调用数据库操作，渲染模板
作者：大一学生助手
创建时间：2026-04-10

这个文件是Web应用的核心，包含了所有路由（URL处理函数）。
每个路由函数只做一件事，代码简单易懂。
所有关键代码都有详细的中文注释。
"""

# 导入Flask模块
# Flask是Python的轻量级Web框架
import os
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from flask_cors import CORS
# 导入时间处理模块
from datetime import datetime

# 导入数据库操作模块
import database

# 导入Gitee API模块
import gitee_api

# 导入代码格式化库（模块6）
import black
import jsbeautifier
import sqlparse
import re

# 创建Flask应用实例
# __name__是当前模块名，Flask需要这个参数来定位资源
app = Flask(__name__)

# 设置密钥
# 密钥用于加密session数据，保证会话安全
# 注意：实际部署时应使用更复杂的密钥
app.secret_key = os.environ.get('SECRET_KEY', 'simple-tool-secret-key-2026')

# 配置CORS（允许跨域请求）
CORS(app, resources={r"/*": {"origins": "*"}})

# 初始化数据库
# 这个函数在应用启动时调用，初始化数据库和创建默认用户
def initialize_database():
    """
    初始化数据库函数
    功能：初始化数据库和创建默认用户
    说明：这个函数在应用启动时调用
    """
    # 调用database模块的初始化函数
    database.init_database()

    # 创建默认用户（如果不存在）
    database.create_default_user()

    print("数据库初始化完成！")

# 立即初始化数据库（应用启动时执行）
initialize_database()

# 首页路由
# @app.route('/') 表示这个函数处理根URL（http://localhost:5000/）
@app.route('/')
def index():
    """
    首页处理函数
    功能：根据用户登录状态跳转到不同页面
    说明：如果用户已登录，跳转到仪表板；否则跳转到登录页面
    """

    # 检查session中是否有user_id
    # session是Flask提供的会话管理工具，可以存储用户信息
    if 'user_id' in session:
        # 用户已登录，跳转到仪表板
        # redirect()函数用于重定向到其他URL
        return redirect(url_for('dashboard'))
    else:
        # 用户未登录，跳转到登录页面
        return redirect(url_for('login'))

# 登录页面路由
# methods=['GET', 'POST'] 表示这个路由接受GET和POST请求
# GET请求：显示登录表单
# POST请求：处理登录表单提交
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录页面处理函数
    功能：显示登录表单和处理登录请求
    说明：这个函数验证用户输入的用户名和密码
    """

    # 检查请求方法
    # 如果是GET请求，显示登录表单
    if request.method == 'GET':
        return render_template('login.html', page_title='用户登录')

    # 如果是POST请求，处理登录表单提交
    # 获取表单数据
    # request.form是一个字典，包含表单提交的所有数据
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    # 检查输入是否为空
    if not username or not password:
        # 如果用户名或密码为空，返回错误信息
        return render_template('login.html',
                             page_title='用户登录',
                             error='用户名和密码不能为空！',
                             username=username)

    # 验证用户登录
    # 调用database模块的verify_user函数验证用户
    user = database.verify_user(username, password)

    if user:
        # 登录成功，设置session
        # session是Flask的会话管理工具，可以存储用户信息
        session['user_id'] = user['id']
        session['username'] = user['username']

        # 跳转到仪表板
        return redirect(url_for('dashboard'))
    else:
        # 登录失败，返回错误信息
        return render_template('login.html',
                             page_title='用户登录',
                             error='用户名或密码错误！',
                             username=username)

# 注册页面路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    注册页面处理函数
    功能：显示注册表单和处理注册请求
    说明：这个函数创建新用户账户
    """

    # 检查请求方法
    # 如果是GET请求，显示注册表单
    if request.method == 'GET':
        return render_template('register.html', page_title='用户注册')

    # 如果是POST请求，处理注册表单提交
    # 获取表单数据
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()

    # 检查输入是否为空
    if not username or not password or not confirm_password:
        return render_template('register.html',
                             page_title='用户注册',
                             error='所有字段都不能为空！',
                             username=username)

    # 检查用户名长度（3-20个字符）
    if len(username) < 3 or len(username) > 20:
        return render_template('register.html',
                             page_title='用户注册',
                             error='用户名必须是3-20个字符！',
                             username=username)

    # 检查密码长度（至少6个字符）
    if len(password) < 6:
        return render_template('register.html',
                             page_title='用户注册',
                             error='密码至少需要6个字符！',
                             username=username)

    # 检查两次输入的密码是否一致
    if password != confirm_password:
        return render_template('register.html',
                             page_title='用户注册',
                             error='两次输入的密码不一致！',
                             username=username)

    # 检查用户名是否已存在
    # 调用database模块的check_username_exists函数
    if database.check_username_exists(username):
        return render_template('register.html',
                             page_title='用户注册',
                             error='用户名已存在，请换一个！',
                             username=username)

    # 创建新用户
    # 调用database模块的create_user函数
    success, error_msg = database.create_user(username, password)

    if success:
        # 注册成功，自动登录并跳转到仪表板
        # 获取新创建的用户信息
        user = database.verify_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            # 如果登录失败，跳转到登录页面
            return redirect(url_for('login'))
    else:
        # 注册失败（可能用户名已存在，虽然我们检查过，但并发情况下可能发生）
        error_detail = error_msg if error_msg else "未知错误"
        return render_template('register.html',
                             page_title='用户注册',
                             error=f'注册失败：{error_detail}',
                             username=username)

# 仪表板路由
@app.route('/dashboard')
def dashboard():
    """
    仪表板处理函数
    功能：显示用户的主控制面板
    说明：这里会显示用户保存的代码和笔记列表
    """

    # 检查用户是否登录
    if 'user_id' not in session:
        # 用户未登录，跳转到登录页面
        return redirect(url_for('login'))

    # 获取用户名（如果session中有）
    username = session.get('username', '用户')

    # 渲染仪表板模板
    # 传递用户名到模板中显示
    return render_template('dashboard.html',
                          page_title='我的仪表板',
                          username=username)

# 关于页面路由
@app.route('/about')
def about():
    """
    关于页面处理函数
    功能：显示关于本工具的信息
    说明：这是一个简单的静态页面
    """
    return render_template('about.html', page_title='关于本工具')

# 用户设置页面路由（模块6）
@app.route('/settings')
def settings_page():
    """
    用户设置页面处理函数
    功能：显示用户设置页面
    说明：这个页面提供密码修改、编辑器设置、格式化选项等功能
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户信息
    username = session.get('username', '用户')
    user_id = session.get('user_id')

    # 获取用户统计信息
    stats = {}
    user_info = {}
    try:
        stats = database.get_user_statistics(user_id) if user_id else {}
        user_info = database.get_user_by_id(user_id) if user_id else {}
    except Exception as e:
        print(f"获取用户信息失败: {str(e)}")

    return render_template('settings.html',
                          page_title='用户设置',
                          username=username,
                          stats=stats,
                          user_info=user_info)

# 登出路由
@app.route('/logout')
def logout():
    """
    登出处理函数
    功能：清除用户session，退出登录
    说明：这个功能在模块2完整实现
    """

    # 清除session中的所有数据
    session.clear()

    # 跳转到首页
    return redirect(url_for('index'))

# 代码列表路由
@app.route('/code/list')
def code_list():
    """
    代码列表处理函数
    功能：显示用户的所有代码片段列表
    说明：这个页面显示用户保存的所有代码片段
    """

    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID
    user_id = session['user_id']

    # 获取用户的代码片段
    code_snippets = database.get_user_code_snippets(user_id)

    # 渲染代码列表模板
    return render_template('code_list.html',
                         page_title='我的代码片段',
                         code_snippets=code_snippets)

# 代码编辑器路由（编辑现有代码或创建新代码）
@app.route('/code')
@app.route('/code/<int:code_id>')
def code_editor(code_id=None):
    """
    代码编辑器处理函数
    功能：显示代码编辑器页面，用于创建或编辑代码片段
    参数：code_id 代码ID（可选，如果不提供则创建新代码）
    说明：如果提供code_id，则编辑现有代码；否则创建新代码
    """

    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID
    user_id = session['user_id']

    # 初始化变量
    code = None
    page_title = '创建新代码'

    # 如果提供了code_id，获取对应的代码片段
    if code_id:
        # 获取代码片段，并验证用户权限
        code = database.get_code_snippet_by_id(code_id, user_id)

        if code:
            # 代码存在且用户有权访问
            page_title = f'编辑代码：{code["title"]}'
        else:
            # 代码不存在或用户无权访问
            return render_template('error.html',
                                 page_title='错误',
                                 error_message='代码不存在或您无权访问此代码！')

    # 渲染代码编辑器模板
    return render_template('code_editor.html',
                         page_title=page_title,
                         code=code)

# 保存代码路由
@app.route('/save_code', methods=['POST'])
def save_code():
    """
    保存代码处理函数
    功能：保存或更新代码片段
    说明：这个函数处理代码的创建和更新
    """

    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID
    user_id = session['user_id']

    # 获取表单数据
    code_id = request.form.get('code_id')
    title = request.form.get('title', '').strip()
    language = request.form.get('language', 'python').strip()
    content = request.form.get('content', '').strip()

    # 检查必填字段
    if not title:
        return "错误：代码标题不能为空！", 400
    if not content:
        return "错误：代码内容不能为空！", 400

    # 保存或更新代码
    if code_id:
        # 更新现有代码
        success, error_msg = database.update_code_snippet(code_id, user_id, title, language, content)
        action = '更新'
    else:
        # 创建新代码
        success, error_msg = database.create_code_snippet(user_id, title, language, content)
        action = '创建'

    # 返回结果
    if success:
        # 保存成功，重定向到代码列表
        return redirect(url_for('code_list'))
    else:
        # 保存失败，返回详细错误信息
        error_detail = error_msg if error_msg else "未知错误"
        return f"错误：{action}代码失败！\n错误详情：{error_detail}", 500

# 删除代码路由
@app.route('/code/delete/<int:code_id>')
def delete_code(code_id):
    """
    删除代码处理函数
    功能：删除指定的代码片段
    参数：code_id 要删除的代码ID
    说明：这个函数删除用户指定的代码片段
    """

    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID
    user_id = session['user_id']

    # 删除代码片段
    success, error_msg = database.delete_code_snippet(code_id, user_id)

    if success:
        # 删除成功，重定向到代码列表
        return redirect(url_for('code_list'))
    else:
        # 删除失败
        error_detail = error_msg if error_msg else "未知错误"
        return render_template('error.html',
                             page_title='错误',
                             error_message=f'删除代码失败！{error_detail}')

# 搜索代码路由
@app.route('/code/search')
def search_code():
    """
    搜索代码处理函数
    功能：搜索用户的代码片段
    说明：这个函数根据关键词搜索代码片段
    """

    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID和搜索关键词
    user_id = session['user_id']
    keyword = request.args.get('q', '').strip()

    # 检查搜索关键词
    if not keyword:
        # 如果关键词为空，重定向到代码列表
        return redirect(url_for('code_list'))

    # 搜索代码片段
    code_snippets = database.search_code_snippets(user_id, keyword)

    # 渲染搜索结果
    return render_template('code_list.html',
                         page_title=f'搜索结果：{keyword}',
                         code_snippets=code_snippets,
                         search_keyword=keyword)

# 笔记列表路由
@app.route('/document/list')
def document_list():
    """
    笔记列表处理函数
    功能：显示用户的所有笔记列表
    说明：这个页面显示用户保存的所有笔记
    """

    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID
    user_id = session['user_id']

    # 获取用户的笔记
    documents = database.get_user_documents(user_id)

    # 渲染笔记列表模板
    return render_template('document_list.html',
                         page_title='我的笔记',
                         documents=documents)

# 笔记编辑器路由（编辑现有笔记或创建新笔记）
@app.route('/markdown')
@app.route('/markdown/<int:doc_id>')
def markdown_editor(doc_id=None):
    """
    笔记编辑器处理函数
    功能：显示笔记编辑器页面，用于创建或编辑笔记
    参数：doc_id 笔记ID（可选，如果不提供则创建新笔记）
    说明：如果提供doc_id，则编辑现有笔记；否则创建新笔记
    """

    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID
    user_id = session['user_id']

    # 初始化变量
    document = None
    page_title = '创建新笔记'

    # 如果提供了doc_id，获取对应的笔记
    if doc_id:
        # 获取笔记，并验证用户权限
        document = database.get_document_by_id(doc_id, user_id)

        if document:
            # 笔记存在且用户有权访问
            page_title = f'编辑笔记：{document["title"]}'
        else:
            # 笔记不存在或用户无权访问
            return render_template('error.html',
                                 page_title='错误',
                                 error_message='笔记不存在或您无权访问此笔记！')

    # 渲染笔记编辑器模板
    return render_template('markdown_editor.html',
                         page_title=page_title,
                         document=document)

# 保存笔记路由
@app.route('/save_document', methods=['POST'])
def save_document():
    """
    保存笔记处理函数
    功能：保存或更新笔记
    说明：这个函数处理笔记的创建和更新
    """

    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID
    user_id = session['user_id']

    # 获取表单数据
    doc_id = request.form.get('doc_id')
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    # 检查必填字段
    if not title:
        return "错误：笔记标题不能为空！", 400
    if not content:
        return "错误：笔记内容不能为空！", 400

    # 保存或更新笔记
    if doc_id:
        # 更新现有笔记
        success, error_msg = database.update_document(doc_id, user_id, title, content)
        action = '更新'
    else:
        # 创建新笔记
        success, error_msg = database.create_document(user_id, title, content)
        action = '创建'

    # 返回结果
    if success:
        # 保存成功，重定向到笔记列表
        return redirect(url_for('document_list'))
    else:
        # 保存失败，返回详细错误信息
        error_detail = error_msg if error_msg else "未知错误"
        return f"错误：{action}笔记失败！\n错误详情：{error_detail}", 500

# 删除笔记路由
@app.route('/document/delete/<int:doc_id>')
def delete_document(doc_id):
    """
    删除笔记处理函数
    功能：删除指定的笔记
    参数：doc_id 要删除的笔记ID
    说明：这个函数删除用户指定的笔记
    """

    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID
    user_id = session['user_id']

    # 删除笔记
    success, error_msg = database.delete_document(doc_id, user_id)

    if success:
        # 删除成功，重定向到笔记列表
        return redirect(url_for('document_list'))
    else:
        # 删除失败
        error_detail = error_msg if error_msg else "未知错误"
        return render_template('error.html',
                             page_title='错误',
                             error_message=f'删除笔记失败！{error_detail}')

# 搜索笔记路由
@app.route('/document/search')
def search_document():
    """
    搜索笔记处理函数
    功能：搜索用户的笔记
    说明：这个函数根据关键词搜索笔记
    """

    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID和搜索关键词
    user_id = session['user_id']
    keyword = request.args.get('q', '').strip()

    # 检查搜索关键词
    if not keyword:
        # 如果关键词为空，重定向到笔记列表
        return redirect(url_for('document_list'))

    # 搜索笔记
    documents = database.search_documents(user_id, keyword)

    # 渲染搜索结果
    return render_template('document_list.html',
                         page_title=f'搜索结果：{keyword}',
                         documents=documents,
                         search_keyword=keyword)

# Gitee页面路由（占位符）
@app.route('/gitee')
def gitee_page():
    """
    Gitee页面处理函数（占位符）
    功能：显示Gitee配置和提交页面
    说明：这个功能在模块5实现
    """
    return render_template('gitee.html', page_title='Gitee提交')

# Gitee配置保存路由
@app.route('/gitee/save_config', methods=['POST'])
def save_gitee_config():
    """
    Gitee配置保存处理函数
    功能：保存用户的Gitee配置（访问令牌和仓库地址）
    说明：验证用户登录，获取表单数据，调用数据库函数保存
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID
    user_id = session['user_id']

    # 获取表单数据
    access_token = request.form.get('access_token', '').strip()
    repo_url = request.form.get('repo_url', '').strip()

    # 验证输入
    if not access_token:
        return "错误：Gitee访问令牌不能为空！", 400
    if not repo_url:
        return "错误：仓库地址不能为空！", 400

    # 保存配置到数据库
    success = database.save_gitee_config(user_id, access_token, repo_url)

    if success:
        return "成功：Gitee配置已保存！"
    else:
        return "错误：保存Gitee配置失败，请稍后重试！", 500

# Gitee配置获取路由
@app.route('/gitee/get_config')
def get_gitee_config():
    """
    Gitee配置获取处理函数
    功能：获取用户的Gitee配置
    说明：返回JSON格式的配置数据，供前端使用
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID
    user_id = session['user_id']

    # 从数据库获取配置
    config = database.get_gitee_config(user_id)

    if config:
        # 返回配置数据（JSON格式）
        # 注意：访问令牌需要保密，这里返回时需要进行处理
        # 在实际应用中，应该只返回部分信息或加密后的信息
        # 这里为了简单，返回完整的配置（包括令牌）
        return {
            'success': True,
            'config': {
                'access_token': config['access_token'],
                'repo_url': config['repo_url']
            }
        }
    else:
        # 没有配置
        return {
            'success': False,
            'message': '未找到Gitee配置'
        }

# Gitee连接测试路由
@app.route('/gitee/test_connection', methods=['POST'])
def test_gitee_connection():
    """
    Gitee连接测试处理函数
    功能：测试Gitee连接是否正常
    说明：验证访问令牌和仓库访问权限
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID
    user_id = session['user_id']

    # 获取表单数据
    access_token = request.form.get('access_token', '').strip()
    repo_url = request.form.get('repo_url', '').strip()

    # 验证输入
    if not access_token or not repo_url:
        return {
            'success': False,
            'message': '访问令牌和仓库地址不能为空！'
        }

    try:
        # 创建Gitee客户端
        client = gitee_api.GiteeClient(access_token)

        # 测试连接
        test_result = client.test_connection(repo_url)

        # 返回测试结果
        return {
            'success': test_result['token_valid'] and test_result['repo_access'],
            'token_valid': test_result['token_valid'],
            'repo_access': test_result['repo_access'],
            'errors': test_result['errors']
        }
    except Exception as e:
        # 测试过程中发生异常
        return {
            'success': False,
            'message': f'测试连接时发生错误：{str(e)}'
        }

# 代码提交到Gitee路由
@app.route('/gitee/submit/code', methods=['POST'])
def submit_code_to_gitee():
    """
    代码提交到Gitee处理函数
    功能：将用户的所有代码片段提交到Gitee
    说明：获取用户代码，调用Gitee API，创建提交记录
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID
    user_id = session['user_id']

    # 获取用户的Gitee配置
    config = database.get_gitee_config(user_id)
    if not config:
        return {
            'success': False,
            'message': '请先配置Gitee访问令牌和仓库地址'
        }

    # 获取用户的所有代码片段
    code_snippets = database.get_user_code_snippets(user_id)
    if not code_snippets:
        return {
            'success': False,
            'message': '没有可提交的代码片段'
        }

    # 获取提交消息（来自请求数据）
    commit_message = request.form.get('commit_message', '').strip()
    if not commit_message:
        commit_message = f'提交代码片段 ({len(code_snippets)}个)'

    # 创建Gitee客户端
    client = gitee_api.GiteeClient(config['access_token'])

    # 准备结果
    results = []
    success_count = 0
    error_count = 0

    # 遍历代码片段并提交
    for code in code_snippets:
        try:
            # 构建文件路径
            # 使用代码ID和标题作为文件名，避免冲突
            file_name = f"code_{code['id']}_{code['title'].replace(' ', '_')}.{code['language']}"
            file_path = f"code_snippets/{file_name}"

            # 构建文件内容
            content = f"# {code['title']}\n# 语言：{code['language']}\n# 创建时间：{code['created_at']}\n\n{code['content']}"

            # 提交到Gitee
            result = client.create_or_update_file(
                config['repo_url'],
                file_path,
                content,
                commit_message
            )

            if result['success']:
                success_count += 1
                results.append({
                    'id': code['id'],
                    'title': code['title'],
                    'success': True,
                    'file_path': file_path,
                    'url': result.get('html_url', '')
                })
            else:
                error_count += 1
                results.append({
                    'id': code['id'],
                    'title': code['title'],
                    'success': False,
                    'error': result.get('error', '未知错误')
                })

        except Exception as e:
            error_count += 1
            results.append({
                'id': code['id'],
                'title': code['title'],
                'success': False,
                'error': str(e)
            })

    # 记录提交历史
    if success_count > 0 or error_count > 0:
        database.create_gitee_commit_record(
            user_id,
            'code',
            len(code_snippets),
            commit_message,
            '',  # Gitee URL（暂无）
            success_count > 0
        )

    # 返回提交结果
    return {
        'success': success_count > 0,
        'message': f'提交完成：成功 {success_count} 个，失败 {error_count} 个',
        'total': len(code_snippets),
        'success_count': success_count,
        'error_count': error_count,
        'results': results
    }

# 笔记提交到Gitee路由
@app.route('/gitee/submit/note', methods=['POST'])
def submit_note_to_gitee():
    """
    笔记提交到Gitee处理函数
    功能：将用户的所有笔记提交到Gitee
    说明：获取用户笔记，调用Gitee API，创建提交记录
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 获取用户ID
    user_id = session['user_id']

    # 获取用户的Gitee配置
    config = database.get_gitee_config(user_id)
    if not config:
        return {
            'success': False,
            'message': '请先配置Gitee访问令牌和仓库地址'
        }

    # 获取用户的所有笔记
    notes = database.get_user_documents(user_id)
    if not notes:
        return {
            'success': False,
            'message': '没有可提交的笔记'
        }

    # 获取提交消息（来自请求数据）
    commit_message = request.form.get('commit_message', '').strip()
    if not commit_message:
        commit_message = f'提交笔记 ({len(notes)}个)'

    # 创建Gitee客户端
    client = gitee_api.GiteeClient(config['access_token'])

    # 准备结果
    results = []
    success_count = 0
    error_count = 0

    # 遍历笔记并提交
    for note in notes:
        try:
            # 构建文件路径
            # 使用笔记ID和标题作为文件名，避免冲突
            file_name = f"note_{note['id']}_{note['title'].replace(' ', '_')}.md"
            file_path = f"notes/{file_name}"

            # 构建文件内容（Markdown格式）
            content = f"# {note['title']}\n\n创建时间：{note['created_at']}\n\n{note['content']}"

            # 提交到Gitee
            result = client.create_or_update_file(
                config['repo_url'],
                file_path,
                content,
                commit_message
            )

            if result['success']:
                success_count += 1
                results.append({
                    'id': note['id'],
                    'title': note['title'],
                    'success': True,
                    'file_path': file_path,
                    'url': result.get('html_url', '')
                })
            else:
                error_count += 1
                results.append({
                    'id': note['id'],
                    'title': note['title'],
                    'success': False,
                    'error': result.get('error', '未知错误')
                })

        except Exception as e:
            error_count += 1
            results.append({
                'id': note['id'],
                'title': note['title'],
                'success': False,
                'error': str(e)
            })

    # 记录提交历史
    if success_count > 0 or error_count > 0:
        database.create_gitee_commit_record(
            user_id,
            'note',
            len(notes),
            commit_message,
            '',  # Gitee URL（暂无）
            success_count > 0
        )

    # 返回提交结果
    return {
        'success': success_count > 0,
        'message': f'提交完成：成功 {success_count} 个，失败 {error_count} 个',
        'total': len(notes),
        'success_count': success_count,
        'error_count': error_count,
        'results': results
    }

# Gitee提交历史获取路由
@app.route('/gitee/get_history')
def get_gitee_history():
    """
    Gitee提交历史获取处理函数
    功能：获取用户的Gitee提交历史记录
    说明：返回JSON格式的提交历史数据
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return {
            'success': False,
            'message': '用户未登录'
        }, 401

    # 获取用户ID
    user_id = session['user_id']

    # 获取限制参数（可选）
    limit = request.args.get('limit', 10, type=int)

    # 从数据库获取提交历史
    try:
        history = database.get_gitee_commit_history(user_id, limit)

        # 格式化时间显示
        for record in history:
            if 'created_at' in record:
                # 将数据库时间戳转换为更友好的格式
                try:
                    # 尝试解析时间戳
                    dt = datetime.strptime(record['created_at'], '%Y-%m-%d %H:%M:%S')
                    record['created_at_formatted'] = dt.strftime('%Y年%m月%d日 %H:%M:%S')
                except:
                    record['created_at_formatted'] = record['created_at']

        return {
            'success': True,
            'history': history,
            'count': len(history)
        }
    except Exception as e:
        # 获取历史记录失败
        return {
            'success': False,
            'message': f'获取提交历史失败：{str(e)}'
        }, 500

# ============================================
# 模块6：代码格式化辅助函数
# ============================================

def format_python_code(code, options):
    """
    使用black格式化Python代码
    参数：
        code: 待格式化的Python代码
        options: 格式化选项字典
    返回：
        格式化后的代码
    """
    try:
        # 获取缩进大小（Black默认为4）
        indent_size = options.get('indent_size', 4)

        # Black不支持直接设置缩进大小，但我们可以通过mode配置
        mode = black.FileMode(
            line_length=options.get('max_line_length', 88),
            string_normalization=options.get('string_normalization', True)
        )

        # 格式化代码
        formatted = black.format_str(code, mode=mode)
        return formatted
    except Exception as e:
        # 格式化失败，返回原始代码
        print(f"Python格式化失败: {str(e)}")
        return code

def format_javascript_code(code, options):
    """
    使用jsbeautifier格式化JavaScript代码
    参数：
        code: 待格式化的JavaScript代码
        options: 格式化选项字典
    返回：
        格式化后的代码
    """
    try:
        # 配置jsbeautifier选项
        opts = jsbeautifier.default_options()
        opts.indent_size = options.get('indent_size', 4)
        opts.indent_char = ' ' if options.get('indent_type', 'spaces') == 'spaces' else '\t'
        opts.space_in_empty_paren = True
        opts.jslint_happy = True
        opts.end_with_newline = options.get('insert_final_newline', True)
        opts.max_preserve_newlines = 2

        # 格式化代码
        formatted = jsbeautifier.beautify(code, opts)
        return formatted
    except Exception as e:
        print(f"JavaScript格式化失败: {str(e)}")
        return code

def format_html_code(code, options):
    """
    使用jsbeautifier格式化HTML代码
    参数：
        code: 待格式化的HTML代码
        options: 格式化选项字典
    返回：
        格式化后的代码
    """
    try:
        # 配置jsbeautifier选项（HTML格式）
        opts = jsbeautifier.default_options()
        opts.indent_size = options.get('indent_size', 4)
        opts.indent_char = ' ' if options.get('indent_type', 'spaces') == 'spaces' else '\t'
        opts.end_with_newline = options.get('insert_final_newline', True)
        opts.max_preserve_newlines = 2

        # 格式化HTML代码
        formatted = jsbeautifier.beautify(code, opts)
        return formatted
    except Exception as e:
        print(f"HTML格式化失败: {str(e)}")
        return code

def format_css_code(code, options):
    """
    使用jsbeautifier格式化CSS代码
    参数：
        code: 待格式化的CSS代码
        options: 格式化选项字典
    返回：
        格式化后的代码
    """
    try:
        # 配置jsbeautifier选项（CSS格式）
        opts = jsbeautifier.default_options()
        opts.indent_size = options.get('indent_size', 4)
        opts.indent_char = ' ' if options.get('indent_type', 'spaces') == 'spaces' else '\t'
        opts.end_with_newline = options.get('insert_final_newline', True)

        # 格式化CSS代码
        formatted = jsbeautifier.beautify(code, opts)
        return formatted
    except Exception as e:
        print(f"CSS格式化失败: {str(e)}")
        return code

def format_sql_code(code, options):
    """
    使用sqlparse格式化SQL代码
    参数：
        code: 待格式化的SQL代码
        options: 格式化选项字典
    返回：
        格式化后的代码
    """
    try:
        # 获取缩进大小
        indent_size = options.get('indent_size', 4)
        indent = ' ' * indent_size

        # 解析SQL
        parsed = sqlparse.parse(code)
        if not parsed:
            return code

        # 重新格式化SQL
        formatted = sqlparse.format(
            code,
            reindent=True,
            indent_width=indent_size,
            keyword_case='upper'
        )
        return formatted
    except Exception as e:
        print(f"SQL格式化失败: {str(e)}")
        return code

def basic_format_code(code, options):
    """
    基础代码格式化（用于不支持的语言）
    参数：
        code: 待格式化的代码
        options: 格式化选项字典
    返回：
        格式化后的代码
    """
    # 获取缩进大小和类型
    indent_size = options.get('indent_size', 4)
    indent_type = options.get('indent_type', 'spaces')

    # 生成缩进字符
    if indent_type == 'spaces':
        indent = ' ' * indent_size
    else:
        indent = '\t'

    # 制表符转换
    formatted = code.replace('\t', indent)

    # 移除行尾空格
    if options.get('trim_trailing_whitespace', True):
        formatted = re.sub(r'[ \t]+$', '', formatted, flags=re.MULTILINE)

    # 确保文件末尾有换行
    if options.get('insert_final_newline', True) and not formatted.endswith('\n'):
        formatted += '\n'

    return formatted

def format_code_with_language(code, language, options):
    """
    根据编程语言调用相应的格式化函数
    参数：
        code: 待格式化的代码
        language: 编程语言
        options: 格式化选项字典
    返回：
        格式化后的代码
    """
    # 语言映射小写
    language = language.lower()

    # 根据语言选择格式化函数
    if language in ['python', 'py']:
        return format_python_code(code, options)
    elif language in ['javascript', 'js', 'node']:
        return format_javascript_code(code, options)
    elif language in ['html', 'htm']:
        return format_html_code(code, options)
    elif language in ['css']:
        return format_css_code(code, options)
    elif language in ['sql']:
        return format_sql_code(code, options)
    else:
        # 其他语言使用基础格式化
        return basic_format_code(code, options)

# ============================================
# 模块6：代码格式化和文件管理功能API路由
# ============================================

# 代码格式化路由
@app.route('/api/format/code', methods=['POST'])
def format_code():
    """
    代码格式化处理函数
    功能：格式化用户提供的代码
    说明：支持多种编程语言，可配置格式化选项
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return {
            'success': False,
            'message': '用户未登录'
        }, 401

    # 获取请求数据
    try:
        data = request.get_json()
        if not data:
            return {
                'success': False,
                'message': '请求数据不能为空'
            }, 400

        code = data.get('code', '')
        language = data.get('language', 'python')
        options = data.get('options', {})

        if not code:
            return {
                'success': False,
                'message': '代码内容不能为空'
            }, 400

        # 尝试获取用户的格式化设置
        try:
            user_id = session.get('user_id')
            if user_id:
                user_settings = database.get_user_settings(user_id)
                if user_settings:
                    # 合并用户设置到选项中
                    options.update({
                        'indent_size': user_settings.get('code_indent_size', options.get('indent_size', 4)),
                        'indent_type': user_settings.get('code_indent_type', options.get('indent_type', 'spaces')),
                        'trim_trailing_whitespace': user_settings.get('trim_trailing_whitespace', options.get('trim_trailing_whitespace', True)),
                        'insert_final_newline': user_settings.get('insert_final_newline', options.get('insert_final_newline', True))
                    })
        except Exception as e:
            # 获取用户设置失败，使用默认选项
            print(f"获取用户格式化设置失败: {str(e)}")

        # 调用代码格式化函数
        formatted_code = format_code_with_language(code, language, options)

        return {
            'success': True,
            'formatted_code': formatted_code,
            'original_length': len(code),
            'formatted_length': len(formatted_code),
            'language': language
        }

    except Exception as e:
        return {
            'success': False,
            'message': f'代码格式化失败：{str(e)}'
        }, 500

# 文件上传路由
@app.route('/api/file/upload', methods=['POST'])
def upload_file():
    """
    文件上传处理函数
    功能：上传并解析用户文件
    说明：支持代码文件和Markdown笔记文件
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return {
            'success': False,
            'message': '用户未登录'
        }, 401

    # 检查是否有文件部分
    if 'file' not in request.files:
        return {
            'success': False,
            'message': '没有上传文件'
        }, 400

    file = request.files['file']

    # 检查文件名
    if file.filename == '':
        return {
            'success': False,
            'message': '没有选择文件'
        }, 400

    # 获取用户ID
    user_id = session['user_id']

    try:
        # 读取文件内容
        content = file.read().decode('utf-8')

        # 获取文件扩展名
        filename = file.filename
        file_extension = filename.split('.')[-1].lower() if '.' in filename else ''

        # 根据扩展名确定文件类型
        if file_extension in ['py', 'js', 'html', 'css', 'java', 'cpp', 'c', 'sql', 'sh', 'bash']:
            file_type = 'code'
            # 从扩展名推断编程语言
            extension_to_language = {
                'py': 'python', 'js': 'javascript', 'html': 'html', 'css': 'css',
                'java': 'java', 'cpp': 'cpp', 'c': 'c', 'sql': 'sql',
                'sh': 'bash', 'bash': 'bash'
            }
            language = extension_to_language.get(file_extension, 'text')
            title = filename.rsplit('.', 1)[0] if '.' in filename else filename
        elif file_extension in ['md', 'txt', 'markdown']:
            file_type = 'document'
            language = 'markdown'
            title = filename.rsplit('.', 1)[0] if '.' in filename else filename
        else:
            file_type = 'unknown'
            language = 'text'
            title = filename

        return {
            'success': True,
            'filename': filename,
            'file_type': file_type,
            'language': language,
            'title': title,
            'content': content,
            'size': len(content)
        }

    except UnicodeDecodeError:
        return {
            'success': False,
            'message': '文件编码错误，请上传UTF-8编码的文本文件'
        }, 400
    except Exception as e:
        return {
            'success': False,
            'message': f'文件上传失败：{str(e)}'
        }, 500

# 文件下载路由
@app.route('/api/file/download', methods=['GET'])
def download_file():
    """
    文件下载处理函数
    功能：生成文件供用户下载
    说明：根据请求参数生成代码文件或笔记文件
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return {
            'success': False,
            'message': '用户未登录'
        }, 401

    # 获取请求参数
    file_type = request.args.get('type', 'code')  # code 或 document
    content = request.args.get('content', '')
    filename = request.args.get('filename', 'download.txt')
    language = request.args.get('language', 'text')

    if not content:
        return {
            'success': False,
            'message': '文件内容不能为空'
        }, 400

    try:
        # 根据文件类型和语言确定文件扩展名
        if file_type == 'code':
            language_to_extension = {
                'python': 'py', 'javascript': 'js', 'html': 'html', 'css': 'css',
                'java': 'java', 'cpp': 'cpp', 'c': 'c', 'sql': 'sql',
                'bash': 'sh', 'text': 'txt'
            }
            extension = language_to_extension.get(language, 'txt')
            if not filename.endswith('.' + extension):
                if '.' in filename:
                    filename = filename.rsplit('.', 1)[0] + '.' + extension
                else:
                    filename = filename + '.' + extension
        else:  # document
            if not filename.endswith('.md'):
                if '.' in filename:
                    filename = filename.rsplit('.', 1)[0] + '.md'
                else:
                    filename = filename + '.md'

        # 创建响应
        from flask import Response
        response = Response(content, mimetype='text/plain')
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'

        # 这里不能直接返回response，因为需要保持JSON API的一致性
        # 改为返回文件信息，前端通过JavaScript触发下载
        return {
            'success': True,
            'filename': filename,
            'content': content,
            'file_type': file_type,
            'size': len(content)
        }

    except Exception as e:
        return {
            'success': False,
            'message': f'文件下载失败：{str(e)}'
        }, 500

# 用户设置获取路由
@app.route('/api/settings', methods=['GET'])
def get_settings():
    """
    用户设置获取处理函数
    功能：获取用户的个性化设置
    说明：返回JSON格式的用户设置数据
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return {
            'success': False,
            'message': '用户未登录'
        }, 401

    # 获取用户ID
    user_id = session['user_id']

    try:
        # 从数据库获取用户设置
        settings = database.get_user_settings(user_id)

        # 获取用户统计信息
        statistics = database.get_user_statistics(user_id)

        return {
            'success': True,
            'settings': settings,
            'statistics': statistics
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'获取用户设置失败：{str(e)}'
        }, 500

# 用户设置保存路由
@app.route('/api/settings', methods=['POST'])
def save_settings():
    """
    用户设置保存处理函数
    功能：保存用户的个性化设置
    说明：接收JSON格式的设置数据并保存到数据库
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return {
            'success': False,
            'message': '用户未登录'
        }, 401

    # 获取用户ID
    user_id = session['user_id']

    # 获取请求数据
    try:
        data = request.get_json()
        if not data:
            return {
                'success': False,
                'message': '请求数据不能为空'
            }, 400

        # 从数据中提取设置
        settings = data.get('settings', {})

        if not settings:
            return {
                'success': False,
                'message': '设置数据不能为空'
            }, 400

        # 保存设置到数据库
        success = database.save_user_settings(user_id, settings)

        if success:
            return {
                'success': True,
                'message': '设置保存成功'
            }
        else:
            return {
                'success': False,
                'message': '设置保存失败'
            }, 500

    except Exception as e:
        return {
            'success': False,
            'message': f'保存设置失败：{str(e)}'
        }, 500

# 用户密码修改路由
@app.route('/api/settings/password', methods=['POST'])
def change_password():
    """
    用户密码修改处理函数
    功能：修改用户密码（需要验证旧密码）
    说明：验证旧密码后更新为新密码
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return {
            'success': False,
            'message': '用户未登录'
        }, 401

    # 获取用户ID
    user_id = session['user_id']

    # 获取请求数据
    try:
        data = request.get_json()
        if not data:
            return {
                'success': False,
                'message': '请求数据不能为空'
            }, 400

        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')

        # 验证输入
        if not old_password or not new_password or not confirm_password:
            return {
                'success': False,
                'message': '所有密码字段都不能为空'
            }, 400

        if new_password != confirm_password:
            return {
                'success': False,
                'message': '新密码和确认密码不一致'
            }, 400

        if len(new_password) < 6:
            return {
                'success': False,
                'message': '新密码至少需要6个字符'
            }, 400

        # 更新密码
        success = database.update_user_password(user_id, old_password, new_password)

        if success:
            return {
                'success': True,
                'message': '密码修改成功'
            }
        else:
            return {
                'success': False,
                'message': '密码修改失败：旧密码不正确或用户不存在'
            }, 400

    except Exception as e:
        return {
            'success': False,
            'message': f'密码修改失败：{str(e)}'
        }, 500

# 用户数据导出路由
@app.route('/api/settings/export', methods=['GET'])
def export_user_data():
    """
    用户数据导出处理函数
    功能：导出用户的所有数据（代码片段和笔记）
    说明：返回JSON格式的完整用户数据
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return {
            'success': False,
            'message': '用户未登录'
        }, 401

    # 获取用户ID
    user_id = session['user_id']

    try:
        # 获取用户的所有代码片段
        code_snippets = database.get_user_code_snippets(user_id)

        # 获取用户的所有笔记
        notes = database.get_user_documents(user_id)

        # 获取用户设置
        settings = database.get_user_settings(user_id)

        # 获取用户统计信息
        statistics = database.get_user_statistics(user_id)

        # 构建完整的数据结构
        user_data = {
            'user_info': {
                'user_id': user_id,
                'export_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'statistics': statistics,
            'settings': settings,
            'code_snippets': code_snippets,
            'notes': notes
        }

        return {
            'success': True,
            'data': user_data,
            'export_time': user_data['user_info']['export_time'],
            'code_count': len(code_snippets),
            'note_count': len(notes)
        }

    except Exception as e:
        return {
            'success': False,
            'message': f'数据导出失败：{str(e)}'
        }, 500

# 健康检查端点（Railway需要）
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}, 200

# 应用启动入口
# 如果直接运行这个文件（而不是作为模块导入），启动Flask开发服务器
if __name__ == '__main__':
    # 从环境变量读取配置
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'

    # 打印启动信息
    print(f"正在启动简单小工具Web应用...")
    print(f"访问地址：http://0.0.0.0:{port}")
    print(f"调试模式: {debug}")
    print("按 Ctrl+C 停止服务器")

    # 启动Flask开发服务器
    # debug根据环境变量设置，代码修改后会自动重启
    # host='0.0.0.0' 表示监听所有网络接口
    # port从环境变量读取，Railway等平台会自动设置
    app.run(debug=debug, host='0.0.0.0', port=port)