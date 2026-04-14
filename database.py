"""
数据库操作模块
功能：所有SQLite数据库操作
作者：大一学生助手
创建时间：2026-04-10

这个文件包含了所有数据库相关的函数。
使用sqlite3模块直接操作数据库，没有使用复杂的ORM。
每个函数都有详细的中文注释，方便理解。
"""

import sqlite3
import os

# 数据库文件路径
# 数据库文件放在data文件夹下，文件名为app.db
# 支持环境变量DATABASE_URL覆盖，适应云端部署环境
import os
DB_PATH = os.environ.get('DATABASE_URL', 'data/app.db')

# 如果默认路径不可写，尝试使用/tmp目录（适用于云端无服务器环境）
if DB_PATH == 'data/app.db':
    # 检查data目录是否可写，如果不可写则使用/tmp目录
    try:
        os.makedirs('data', exist_ok=True)
        # 尝试创建测试文件检查可写性
        test_file = 'data/.write_test'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
    except (OSError, IOError):
        # 如果data目录不可写，使用/tmp目录
        DB_PATH = '/tmp/app.db'
        print(f"数据目录不可写，使用临时数据库路径：{DB_PATH}")
        # 确保/tmp目录存在
        try:
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        except:
            pass  # /tmp通常已存在

def init_database():
    """
    初始化数据库函数
    功能：创建所有需要的表（如果表不存在）
    说明：这个函数会在应用第一次运行时自动创建数据库和表
    """

    # 创建数据库文件所在目录（如果不存在）
    # os.makedirs函数会创建目录，如果目录已存在也不会报错
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:  # 如果路径包含目录部分
        os.makedirs(db_dir, exist_ok=True)

    # 连接数据库
    # sqlite3.connect()函数用于连接SQLite数据库
    # 如果数据库文件不存在，会自动创建
    conn = sqlite3.connect(DB_PATH)

    # 创建游标对象
    # 游标用于执行SQL语句
    cursor = conn.cursor()

    # 创建用户表（users）
    # 这个表用来存储用户信息
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 用户ID，自动增长
            username TEXT UNIQUE NOT NULL,             -- 用户名，不能重复
            password TEXT NOT NULL,                    -- 密码
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 创建时间
        )
    ''')

    # 创建代码片段表（code_snippets）
    # 这个表用来存储用户保存的代码
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS code_snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 代码ID，自动增长
            user_id INTEGER NOT NULL,                  -- 用户ID，关联用户表
            title TEXT NOT NULL,                       -- 代码标题
            language TEXT NOT NULL,                    -- 编程语言
            content TEXT NOT NULL,                     -- 代码内容
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 更新时间
            FOREIGN KEY (user_id) REFERENCES users(id)  -- 外键关联用户表
        )
    ''')

    # 创建文档笔记表（documents）
    # 这个表用来存储用户的Markdown笔记
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 笔记ID，自动增长
            user_id INTEGER NOT NULL,                  -- 用户ID，关联用户表
            title TEXT NOT NULL,                       -- 笔记标题
            content TEXT NOT NULL,                     -- 笔记内容（Markdown格式）
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 更新时间
            FOREIGN KEY (user_id) REFERENCES users(id)  -- 外键关联用户表
        )
    ''')

    # 创建Gitee配置表（gitee_config）
    # 这个表用来存储用户的Gitee配置信息
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gitee_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 配置ID，自动增长
            user_id INTEGER NOT NULL,                  -- 用户ID，关联用户表
            access_token TEXT NOT NULL,                -- Gitee个人访问令牌
            repo_url TEXT NOT NULL,                    -- 仓库地址
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
            FOREIGN KEY (user_id) REFERENCES users(id)  -- 外键关联用户表
        )
    ''')

    # 创建Gitee提交记录表（gitee_commits）
    # 这个表用来存储用户的Gitee提交历史
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gitee_commits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 记录ID，自动增长
            user_id INTEGER NOT NULL,                  -- 用户ID，关联用户表
            commit_type TEXT NOT NULL,                 -- 提交类型：code（代码）或note（笔记）
            item_count INTEGER NOT NULL,               -- 提交的项目数量
            commit_message TEXT NOT NULL,              -- 提交消息
            gitee_url TEXT,                            -- Gitee提交的URL
            success BOOLEAN NOT NULL,                  -- 是否成功
            error_message TEXT,                        -- 错误信息（如果失败）
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
            FOREIGN KEY (user_id) REFERENCES users(id)  -- 外键关联用户表
        )
    ''')

    # 创建用户设置表（user_settings）
    # 这个表用来存储用户的个性化设置和偏好
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 设置ID，自动增长
            user_id INTEGER NOT NULL,                  -- 用户ID，关联用户表
            theme TEXT DEFAULT 'light',                -- 主题：light（浅色）或 dark（深色）
            editor_font_size INTEGER DEFAULT 14,       -- 编辑器字体大小（像素）
            default_language TEXT DEFAULT 'python',    -- 默认编程语言
            code_indent_size INTEGER DEFAULT 4,        -- 代码缩进大小：2、4或8
            code_indent_type TEXT DEFAULT 'spaces',    -- 缩进类型：spaces（空格）或 tabs（制表符）
            auto_format BOOLEAN DEFAULT FALSE,         -- 是否自动格式化代码
            auto_save BOOLEAN DEFAULT TRUE,            -- 是否自动保存
            trim_trailing_whitespace BOOLEAN DEFAULT TRUE,  -- 是否移除行尾空格
            insert_final_newline BOOLEAN DEFAULT TRUE, -- 是否在文件末尾添加换行
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 更新时间
            FOREIGN KEY (user_id) REFERENCES users(id),  -- 外键关联用户表
            UNIQUE(user_id)  -- 每个用户只能有一条设置记录
        )
    ''')

    # 提交更改
    # conn.commit()将所有的更改保存到数据库
    conn.commit()

    # 关闭数据库连接
    # 使用完数据库后一定要关闭连接
    conn.close()

    # 打印成功信息
    print("数据库初始化完成！所有表已创建。")
    print(f"数据库文件位置：{DB_PATH}")

def create_default_user():
    """
    创建默认用户函数
    功能：如果用户表为空，创建一个默认用户
    说明：这个函数是为了方便测试，实际使用中用户应该自己注册
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 检查用户表是否已经有用户
    # 使用SELECT COUNT(*)统计用户数量
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]  # fetchone()返回一个元组，取第一个值

    # 如果用户数量为0，创建默认用户
    if user_count == 0:
        # 插入默认用户
        # 用户名：admin，密码：123456
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                      ('admin', '123456'))
        conn.commit()
        print("已创建默认用户：用户名=admin，密码=123456")

    # 关闭数据库连接
    conn.close()

def verify_user(username, password):
    """
    验证用户登录函数
    功能：验证用户名和密码是否正确
    参数：username 用户名, password 密码
    返回值：如果验证成功，返回用户信息字典；否则返回None
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 设置row_factory，使返回结果为字典格式
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 查询用户
    # SQL语句：从users表中选择用户名和密码匹配的记录
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                  (username, password))

    # 获取查询结果
    user = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

    # 如果找到用户，返回用户信息字典；否则返回None
    if user:
        return dict(user)  # 将Row对象转换为字典
    else:
        return None

def create_user(username, password):
    """
    创建新用户函数
    功能：在数据库中创建新用户
    参数：username 用户名, password 密码
    返回值：如果创建成功返回(True, None)，失败返回(False, 错误信息)
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 插入新用户
        # SQL语句：向users表插入新的用户名和密码
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                      (username, password))

        # 提交更改
        conn.commit()

        # 创建成功
        print(f"用户创建成功：{username}")
        return (True, None)
    except sqlite3.IntegrityError:
        # 如果用户名已存在，会抛出IntegrityError异常
        error_msg = f"用户名已存在：{username}"
        print(error_msg)
        return (False, error_msg)
    except Exception as e:
        # 其他错误
        error_msg = f"创建用户失败：{e}"
        print(error_msg)
        return (False, error_msg)
    finally:
        # 关闭数据库连接
        conn.close()

def check_username_exists(username):
    """
    检查用户名是否存在函数
    功能：检查指定的用户名是否已存在
    参数：username 用户名
    返回值：如果用户名存在返回True，否则返回False
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 查询用户名是否存在
    # SQL语句：统计指定用户名的数量
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))

    # 获取查询结果
    count = cursor.fetchone()[0]

    # 关闭数据库连接
    conn.close()

    # 如果count大于0，表示用户名已存在
    return count > 0

def get_user_by_id(user_id):
    """
    根据用户ID获取用户信息函数
    功能：根据用户ID获取用户信息
    参数：user_id 用户ID
    返回值：用户信息字典，如果用户不存在返回None
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 查询用户
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))

    # 获取查询结果
    user = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

    # 如果找到用户，返回用户信息字典；否则返回None
    if user:
        return dict(user)
    else:
        return None

def get_user_by_username(username):
    """
    根据用户名获取用户信息函数
    功能：根据用户名获取用户信息
    参数：username 用户名
    返回值：用户信息字典，如果用户不存在返回None
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 查询用户
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))

    # 获取查询结果
    user = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

    # 如果找到用户，返回用户信息字典；否则返回None
    if user:
        return dict(user)
    else:
        return None

def create_code_snippet(user_id, title, language, content):
    """
    创建代码片段函数
    功能：在数据库中创建新的代码片段
    参数：user_id 用户ID, title 代码标题, language 编程语言, content 代码内容
    返回值：如果创建成功返回(True, None)，失败返回(False, 错误信息)
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 插入新代码片段
        # SQL语句：向code_snippets表插入新的代码片段
        cursor.execute('''
            INSERT INTO code_snippets (user_id, title, language, content)
            VALUES (?, ?, ?, ?)
        ''', (user_id, title, language, content))

        # 提交更改
        conn.commit()

        # 创建成功
        print(f"代码片段创建成功：{title}")
        return (True, None)
    except Exception as e:
        # 创建失败
        error_msg = f"创建代码片段失败：{e}"
        print(error_msg)
        return (False, error_msg)
    finally:
        # 关闭数据库连接
        conn.close()

def get_user_code_snippets(user_id):
    """
    获取用户代码片段函数
    功能：获取指定用户的所有代码片段
    参数：user_id 用户ID
    返回值：代码片段列表（字典列表），如果没有返回空列表
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 查询用户的代码片段
    # 按更新时间降序排列，最新的在前面
    cursor.execute('''
        SELECT * FROM code_snippets
        WHERE user_id = ?
        ORDER BY updated_at DESC
    ''', (user_id,))

    # 获取所有结果
    code_snippets = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    # 将Row对象转换为字典列表
    return [dict(code) for code in code_snippets]

def get_code_snippet_by_id(code_id, user_id=None):
    """
    根据ID获取代码片段函数
    功能：根据代码ID获取代码片段，可选用户ID验证
    参数：code_id 代码ID, user_id 用户ID（可选，用于验证权限）
    返回值：代码片段字典，如果不存在或无权访问返回None
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 构建SQL查询
    if user_id:
        # 如果提供了user_id，验证用户权限
        cursor.execute('''
            SELECT * FROM code_snippets
            WHERE id = ? AND user_id = ?
        ''', (code_id, user_id))
    else:
        # 如果没有提供user_id，只根据ID查询
        cursor.execute('SELECT * FROM code_snippets WHERE id = ?', (code_id,))

    # 获取查询结果
    code_snippet = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

    # 如果找到代码片段，返回字典；否则返回None
    if code_snippet:
        return dict(code_snippet)
    else:
        return None

def update_code_snippet(code_id, user_id, title, language, content):
    """
    更新代码片段函数
    功能：更新指定的代码片段
    参数：code_id 代码ID, user_id 用户ID, title 代码标题, language 编程语言, content 代码内容
    返回值：如果更新成功返回(True, None)，失败返回(False, 错误信息)
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 更新代码片段
        # SQL语句：更新code_snippets表中的代码片段
        cursor.execute('''
            UPDATE code_snippets
            SET title = ?, language = ?, content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        ''', (title, language, content, code_id, user_id))

        # 提交更改
        conn.commit()

        # 检查是否更新了记录
        rows_updated = cursor.rowcount

        if rows_updated > 0:
            print(f"代码片段更新成功：ID={code_id}")
            return (True, None)
        else:
            error_msg = f"代码片段不存在或无权访问：ID={code_id}"
            print(error_msg)
            return (False, error_msg)
    except Exception as e:
        # 更新失败
        error_msg = f"更新代码片段失败：{e}"
        print(error_msg)
        return (False, error_msg)
    finally:
        # 关闭数据库连接
        conn.close()

def delete_code_snippet(code_id, user_id):
    """
    删除代码片段函数
    功能：删除指定的代码片段
    参数：code_id 代码ID, user_id 用户ID
    返回值：如果删除成功返回(True, None)，失败返回(False, 错误信息)
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 删除代码片段
        # SQL语句：从code_snippets表中删除代码片段
        cursor.execute('DELETE FROM code_snippets WHERE id = ? AND user_id = ?',
                      (code_id, user_id))

        # 提交更改
        conn.commit()

        # 检查是否删除了记录
        rows_deleted = cursor.rowcount

        if rows_deleted > 0:
            print(f"代码片段删除成功：ID={code_id}")
            return (True, None)
        else:
            error_msg = f"代码片段不存在或无权访问：ID={code_id}"
            print(error_msg)
            return (False, error_msg)
    except Exception as e:
        # 删除失败
        error_msg = f"删除代码片段失败：{e}"
        print(error_msg)
        return (False, error_msg)
    finally:
        # 关闭数据库连接
        conn.close()

def search_code_snippets(user_id, keyword):
    """
    搜索代码片段函数
    功能：搜索用户代码片段（标题和内容）
    参数：user_id 用户ID, keyword 搜索关键词
    返回值：匹配的代码片段列表（字典列表）
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 构建搜索关键词（添加通配符）
    search_pattern = f'%{keyword}%'

    # 搜索代码片段（标题或内容包含关键词）
    cursor.execute('''
        SELECT * FROM code_snippets
        WHERE user_id = ? AND (title LIKE ? OR content LIKE ?)
        ORDER BY updated_at DESC
    ''', (user_id, search_pattern, search_pattern))

    # 获取所有结果
    code_snippets = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    # 将Row对象转换为字典列表
    return [dict(code) for code in code_snippets]

def create_document(user_id, title, content):
    """
    创建笔记函数
    功能：在数据库中创建新的笔记（Markdown格式）
    参数：user_id 用户ID, title 笔记标题, content 笔记内容（Markdown）
    返回值：如果创建成功返回(True, None)，失败返回(False, 错误信息)
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 插入新笔记
        # SQL语句：向documents表插入新的笔记
        cursor.execute('''
            INSERT INTO documents (user_id, title, content)
            VALUES (?, ?, ?)
        ''', (user_id, title, content))

        # 提交更改
        conn.commit()

        # 创建成功
        print(f"笔记创建成功：{title}")
        return (True, None)
    except Exception as e:
        # 创建失败
        error_msg = f"创建笔记失败：{e}"
        print(error_msg)
        return (False, error_msg)
    finally:
        # 关闭数据库连接
        conn.close()

def get_user_documents(user_id):
    """
    获取用户笔记函数
    功能：获取指定用户的所有笔记
    参数：user_id 用户ID
    返回值：笔记列表（字典列表），如果没有返回空列表
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 查询用户的笔记
    # 按更新时间降序排列，最新的在前面
    cursor.execute('''
        SELECT * FROM documents
        WHERE user_id = ?
        ORDER BY updated_at DESC
    ''', (user_id,))

    # 获取所有结果
    documents = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    # 将Row对象转换为字典列表
    return [dict(doc) for doc in documents]

def get_document_by_id(doc_id, user_id=None):
    """
    根据ID获取笔记函数
    功能：根据笔记ID获取笔记，可选用户ID验证
    参数：doc_id 笔记ID, user_id 用户ID（可选，用于验证权限）
    返回值：笔记字典，如果不存在或无权访问返回None
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 构建SQL查询
    if user_id:
        # 如果提供了user_id，验证用户权限
        cursor.execute('''
            SELECT * FROM documents
            WHERE id = ? AND user_id = ?
        ''', (doc_id, user_id))
    else:
        # 如果没有提供user_id，只根据ID查询
        cursor.execute('SELECT * FROM documents WHERE id = ?', (doc_id,))

    # 获取查询结果
    document = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

    # 如果找到笔记，返回字典；否则返回None
    if document:
        return dict(document)
    else:
        return None

def update_document(doc_id, user_id, title, content):
    """
    更新笔记函数
    功能：更新指定的笔记
    参数：doc_id 笔记ID, user_id 用户ID, title 笔记标题, content 笔记内容
    返回值：如果更新成功返回(True, None)，失败返回(False, 错误信息)
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 更新笔记
        # SQL语句：更新documents表中的笔记
        cursor.execute('''
            UPDATE documents
            SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        ''', (title, content, doc_id, user_id))

        # 提交更改
        conn.commit()

        # 检查是否更新了记录
        rows_updated = cursor.rowcount

        if rows_updated > 0:
            print(f"笔记更新成功：ID={doc_id}")
            return (True, None)
        else:
            error_msg = f"笔记不存在或无权访问：ID={doc_id}"
            print(error_msg)
            return (False, error_msg)
    except Exception as e:
        # 更新失败
        error_msg = f"更新笔记失败：{e}"
        print(error_msg)
        return (False, error_msg)
    finally:
        # 关闭数据库连接
        conn.close()

def delete_document(doc_id, user_id):
    """
    删除笔记函数
    功能：删除指定的笔记
    参数：doc_id 笔记ID, user_id 用户ID
    返回值：如果删除成功返回(True, None)，失败返回(False, 错误信息)
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 删除笔记
        # SQL语句：从documents表中删除笔记
        cursor.execute('DELETE FROM documents WHERE id = ? AND user_id = ?',
                      (doc_id, user_id))

        # 提交更改
        conn.commit()

        # 检查是否删除了记录
        rows_deleted = cursor.rowcount

        if rows_deleted > 0:
            print(f"笔记删除成功：ID={doc_id}")
            return (True, None)
        else:
            error_msg = f"笔记不存在或无权访问：ID={doc_id}"
            print(error_msg)
            return (False, error_msg)
    except Exception as e:
        # 删除失败
        error_msg = f"删除笔记失败：{e}"
        print(error_msg)
        return (False, error_msg)
    finally:
        # 关闭数据库连接
        conn.close()

def search_documents(user_id, keyword):
    """
    搜索笔记函数
    功能：搜索用户笔记（标题和内容）
    参数：user_id 用户ID, keyword 搜索关键词
    返回值：匹配的笔记列表（字典列表）
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 构建搜索关键词（添加通配符）
    search_pattern = f'%{keyword}%'

    # 搜索笔记（标题或内容包含关键词）
    cursor.execute('''
        SELECT * FROM documents
        WHERE user_id = ? AND (title LIKE ? OR content LIKE ?)
        ORDER BY updated_at DESC
    ''', (user_id, search_pattern, search_pattern))

    # 获取所有结果
    documents = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    # 将Row对象转换为字典列表
    return [dict(doc) for doc in documents]

def save_gitee_config(user_id, access_token, repo_url):
    """
    保存Gitee配置函数
    功能：保存用户的Gitee访问令牌和仓库地址
    参数：user_id 用户ID, access_token Gitee访问令牌, repo_url 仓库地址
    返回值：如果保存成功返回True，失败返回False
    说明：每个用户只能保存一个配置，如果已存在则更新
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 先删除用户现有配置（如果存在）
        cursor.execute('DELETE FROM gitee_config WHERE user_id = ?', (user_id,))

        # 插入新配置
        cursor.execute('''
            INSERT INTO gitee_config (user_id, access_token, repo_url)
            VALUES (?, ?, ?)
        ''', (user_id, access_token, repo_url))

        # 提交更改
        conn.commit()

        # 保存成功
        print(f"Gitee配置保存成功：user_id={user_id}")
        success = True
    except Exception as e:
        # 保存失败
        print(f"保存Gitee配置失败：{e}")
        success = False
    finally:
        # 关闭数据库连接
        conn.close()

    return success

def get_gitee_config(user_id):
    """
    获取Gitee配置函数
    功能：获取用户的Gitee配置
    参数：user_id 用户ID
    返回值：Gitee配置字典，如果不存在返回None
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 查询用户的Gitee配置
    cursor.execute('SELECT * FROM gitee_config WHERE user_id = ?', (user_id,))

    # 获取查询结果
    config = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

    # 如果找到配置，返回字典；否则返回None
    if config:
        return dict(config)
    else:
        return None

def delete_gitee_config(user_id):
    """
    删除Gitee配置函数
    功能：删除用户的Gitee配置
    参数：user_id 用户ID
    返回值：如果删除成功返回True，失败返回False
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 删除配置
        cursor.execute('DELETE FROM gitee_config WHERE user_id = ?', (user_id,))

        # 提交更改
        conn.commit()

        # 检查是否删除了记录
        rows_deleted = cursor.rowcount

        if rows_deleted > 0:
            print(f"Gitee配置删除成功：user_id={user_id}")
            success = True
        else:
            print(f"Gitee配置不存在：user_id={user_id}")
            success = False
    except Exception as e:
        # 删除失败
        print(f"删除Gitee配置失败：{e}")
        success = False
    finally:
        # 关闭数据库连接
        conn.close()

    return success

def create_gitee_commit_record(user_id, commit_type, item_count, commit_message, gitee_url, success):
    """
    创建Gitee提交记录函数
    功能：记录Gitee提交历史
    参数：
        user_id 用户ID
        commit_type 提交类型：'code'（代码）或'note'（笔记）
        item_count 提交的项目数量
        commit_message 提交消息
        gitee_url Gitee提交的URL（可选）
        success 是否成功（True/False）
    返回值：如果创建成功返回True，失败返回False
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 插入提交记录
        cursor.execute('''
            INSERT INTO gitee_commits (user_id, commit_type, item_count, commit_message, gitee_url, success)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, commit_type, item_count, commit_message, gitee_url, success))

        # 提交更改
        conn.commit()

        # 创建成功
        print(f"Gitee提交记录创建成功：user_id={user_id}, type={commit_type}")
        success = True
    except Exception as e:
        # 创建失败
        print(f"创建Gitee提交记录失败：{e}")
        success = False
    finally:
        # 关闭数据库连接
        conn.close()

    return success

def get_gitee_commit_history(user_id, limit=10):
    """
    获取Gitee提交历史函数
    功能：获取用户的Gitee提交记录
    参数：user_id 用户ID, limit 返回记录数量限制
    返回值：提交历史列表（字典列表）
    """

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 查询用户的提交历史，按时间倒序排列
    cursor.execute('''
        SELECT * FROM gitee_commits
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    ''', (user_id, limit))

    # 获取所有结果
    commits = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    # 将Row对象转换为字典列表
    return [dict(commit) for commit in commits]

def save_user_settings(user_id, settings):
    """
    保存用户设置函数
    功能：保存或更新用户的个性化设置
    参数：user_id 用户ID, settings 设置字典
    返回值：如果保存成功返回True，失败返回False
    """
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 首先检查是否已存在该用户的设置
        cursor.execute('SELECT COUNT(*) FROM user_settings WHERE user_id = ?', (user_id,))
        count = cursor.fetchone()[0]

        # 准备设置数据
        theme = settings.get('theme', 'light')
        editor_font_size = settings.get('editor_font_size', 14)
        default_language = settings.get('default_language', 'python')
        code_indent_size = settings.get('code_indent_size', 4)
        code_indent_type = settings.get('code_indent_type', 'spaces')
        auto_format = 1 if settings.get('auto_format', False) else 0
        auto_save = 1 if settings.get('auto_save', True) else 0
        trim_trailing_whitespace = 1 if settings.get('trim_trailing_whitespace', True) else 0
        insert_final_newline = 1 if settings.get('insert_final_newline', True) else 0

        if count == 0:
            # 插入新设置
            cursor.execute('''
                INSERT INTO user_settings (
                    user_id, theme, editor_font_size, default_language,
                    code_indent_size, code_indent_type, auto_format, auto_save,
                    trim_trailing_whitespace, insert_final_newline
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, theme, editor_font_size, default_language,
                code_indent_size, code_indent_type, auto_format, auto_save,
                trim_trailing_whitespace, insert_final_newline
            ))
        else:
            # 更新现有设置
            cursor.execute('''
                UPDATE user_settings SET
                    theme = ?,
                    editor_font_size = ?,
                    default_language = ?,
                    code_indent_size = ?,
                    code_indent_type = ?,
                    auto_format = ?,
                    auto_save = ?,
                    trim_trailing_whitespace = ?,
                    insert_final_newline = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (
                theme, editor_font_size, default_language,
                code_indent_size, code_indent_type, auto_format, auto_save,
                trim_trailing_whitespace, insert_final_newline, user_id
            ))

        # 提交更改
        conn.commit()
        success = True
        print(f"用户设置保存成功：user_id={user_id}")
    except Exception as e:
        # 保存失败
        print(f"保存用户设置失败：{e}")
        success = False
    finally:
        # 关闭数据库连接
        conn.close()

    return success

def get_user_settings(user_id):
    """
    获取用户设置函数
    功能：获取用户的个性化设置
    参数：user_id 用户ID
    返回值：用户设置字典，如果不存在返回默认设置
    """
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 查询用户设置
    cursor.execute('SELECT * FROM user_settings WHERE user_id = ?', (user_id,))
    settings = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

    if settings:
        # 将Row对象转换为字典，并转换布尔值
        settings_dict = dict(settings)
        # 将SQLite的整数布尔值转换为Python布尔值
        bool_fields = ['auto_format', 'auto_save', 'trim_trailing_whitespace', 'insert_final_newline']
        for field in bool_fields:
            if field in settings_dict:
                settings_dict[field] = bool(settings_dict[field])
        return settings_dict
    else:
        # 返回默认设置
        return {
            'theme': 'light',
            'editor_font_size': 14,
            'default_language': 'python',
            'code_indent_size': 4,
            'code_indent_type': 'spaces',
            'auto_format': False,
            'auto_save': True,
            'trim_trailing_whitespace': True,
            'insert_final_newline': True
        }

def update_user_password(user_id, old_password, new_password):
    """
    更新用户密码函数
    功能：更新用户密码（需要验证旧密码）
    参数：user_id 用户ID, old_password 旧密码, new_password 新密码
    返回值：如果更新成功返回True，失败返回False
    """
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 首先验证旧密码
        cursor.execute('SELECT password FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()

        if not result:
            # 用户不存在
            print(f"用户不存在：user_id={user_id}")
            return False

        current_password = result[0]
        if current_password != old_password:
            # 旧密码不正确
            print(f"旧密码不正确：user_id={user_id}")
            return False

        # 更新密码
        cursor.execute('UPDATE users SET password = ? WHERE id = ?', (new_password, user_id))
        conn.commit()

        success = cursor.rowcount > 0
        if success:
            print(f"密码更新成功：user_id={user_id}")
        else:
            print(f"密码更新失败：user_id={user_id}")

        return success
    except Exception as e:
        # 更新失败
        print(f"更新密码失败：{e}")
        return False
    finally:
        # 关闭数据库连接
        conn.close()

def get_user_statistics(user_id):
    """
    获取用户统计数据函数
    功能：获取用户的使用统计信息
    参数：user_id 用户ID
    返回值：统计信息字典
    """
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # 获取代码片段数量
        cursor.execute('SELECT COUNT(*) FROM code_snippets WHERE user_id = ?', (user_id,))
        code_count = cursor.fetchone()[0]

        # 获取笔记数量
        cursor.execute('SELECT COUNT(*) FROM documents WHERE user_id = ?', (user_id,))
        note_count = cursor.fetchone()[0]

        # 获取Gitee提交次数
        cursor.execute('SELECT COUNT(*) FROM gitee_commits WHERE user_id = ? AND success = 1', (user_id,))
        gitee_commit_count = cursor.fetchone()[0]

        # 获取用户注册时间
        cursor.execute('SELECT created_at FROM users WHERE id = ?', (user_id,))
        user_result = cursor.fetchone()
        registration_date = user_result[0] if user_result else '未知'

        # 获取最近登录时间（这里简化处理，实际应用中应该有登录记录表）
        # 使用用户最后一次保存代码或笔记的时间作为最近活动时间
        cursor.execute('''
            SELECT MAX(updated_at) FROM (
                SELECT updated_at FROM code_snippets WHERE user_id = ?
                UNION ALL
                SELECT updated_at FROM documents WHERE user_id = ?
            )
        ''', (user_id, user_id))
        last_activity_result = cursor.fetchone()
        last_activity = last_activity_result[0] if last_activity_result and last_activity_result[0] else '未知'

        # 构建统计信息字典
        statistics = {
            'code_count': code_count,
            'note_count': note_count,
            'gitee_commit_count': gitee_commit_count,
            'registration_date': registration_date,
            'last_activity': last_activity,
            'total_items': code_count + note_count
        }

        return statistics
    except Exception as e:
        # 获取统计信息失败
        print(f"获取用户统计信息失败：{e}")
        return {}
    finally:
        # 关闭数据库连接
        conn.close()

# 测试代码
# 如果直接运行这个文件，会初始化数据库并创建默认用户
if __name__ == '__main__':
    # 调用初始化函数
    init_database()

    # 调用创建默认用户函数
    create_default_user()

    print("数据库模块测试完成！")