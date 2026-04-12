/*
JavaScript文件：main.js
功能：处理网页的所有交互功能
作者：大一学生助手
创建时间：2026-04-10

这个文件包含了所有JavaScript代码。
使用原生JavaScript，没有使用任何框架。
所有函数都有详细的中文注释。
*/

// 等待页面完全加载后执行代码
// DOMContentLoaded事件表示HTML文档已完全加载和解析
document.addEventListener('DOMContentLoaded', function() {
    console.log('页面加载完成，开始初始化...');

    // 初始化所有功能
    initPage();

    // 绑定所有按钮事件
    bindEvents();

    // 显示欢迎消息
    showWelcomeMessage();
});

/**
 * 初始化页面函数
 * 功能：执行页面初始化操作
 * 说明：这个函数在页面加载完成后调用
 */
function initPage() {
    console.log('正在初始化页面...');

    // 检查用户登录状态
    // 通过检查页面元素来判断用户是否登录
    const userArea = document.querySelector('.user-area');
    if (userArea) {
        const usernameSpan = userArea.querySelector('.username');
        if (usernameSpan) {
            console.log('用户已登录：' + usernameSpan.textContent);
        } else {
            console.log('用户未登录');
        }
    }

    // 初始化代码编辑器区域（如果存在）
    initCodeEditor();

    // 初始化Markdown编辑器区域（如果存在）
    initMarkdownEditor();

    // 初始化Gitee页面（如果存在）
    initGiteePage();

    console.log('页面初始化完成！');
}

/**
 * 绑定事件函数
 * 功能：为页面上的按钮和表单绑定事件处理函数
 * 说明：这个函数绑定所有交互元素的事件
 */
function bindEvents() {
    console.log('正在绑定事件...');

    // 绑定代码保存按钮（如果存在）
    const saveCodeButtons = document.querySelectorAll('.save-code-btn');
    saveCodeButtons.forEach(function(button) {
        button.addEventListener('click', saveCode);
        console.log('已绑定代码保存按钮：', button);
    });

    // 绑定代码格式化按钮（如果存在）
    const formatCodeButtons = document.querySelectorAll('.format-code-btn');
    formatCodeButtons.forEach(function(button) {
        button.addEventListener('click', formatCode);
        console.log('已绑定代码格式化按钮：', button);
    });

    // 绑定文件导入按钮（如果存在）
    const importFileButtons = document.querySelectorAll('.import-file-btn');
    importFileButtons.forEach(function(button) {
        button.addEventListener('change', importFile);
        console.log('已绑定文件导入按钮：', button);
    });

    // 绑定文件导出按钮（如果存在）
    const exportFileButtons = document.querySelectorAll('.export-file-btn');
    exportFileButtons.forEach(function(button) {
        button.addEventListener('click', exportFile);
        console.log('已绑定文件导出按钮：', button);
    });

    // 绑定Markdown预览切换按钮（如果存在）
    const previewToggleButtons = document.querySelectorAll('.preview-toggle-btn');
    previewToggleButtons.forEach(function(button) {
        button.addEventListener('click', toggleMarkdownPreview);
        console.log('已绑定Markdown预览切换按钮：', button);
    });

    // 绑定笔记保存按钮（如果存在）
    const saveNoteButtons = document.querySelectorAll('.save-note-btn');
    saveNoteButtons.forEach(function(button) {
        button.addEventListener('click', saveDocument);
        console.log('已绑定笔记保存按钮：', button);
    });

    // 绑定Gitee相关按钮（如果存在）
    const saveGiteeConfigBtn = document.getElementById('save-gitee-config-btn');
    if (saveGiteeConfigBtn) {
        saveGiteeConfigBtn.addEventListener('click', saveGiteeConfig);
        console.log('已绑定Gitee配置保存按钮：', saveGiteeConfigBtn);
    }

    const testGiteeConnectionBtn = document.getElementById('test-gitee-connection-btn');
    if (testGiteeConnectionBtn) {
        testGiteeConnectionBtn.addEventListener('click', testGiteeConnection);
        console.log('已绑定Gitee连接测试按钮：', testGiteeConnectionBtn);
    }

    const submitCodeToGiteeBtn = document.getElementById('submit-code-to-gitee-btn');
    if (submitCodeToGiteeBtn) {
        submitCodeToGiteeBtn.addEventListener('click', submitAllCodeToGitee);
        console.log('已绑定代码提交按钮：', submitCodeToGiteeBtn);
    }

    const submitNoteToGiteeBtn = document.getElementById('submit-note-to-gitee-btn');
    if (submitNoteToGiteeBtn) {
        submitNoteToGiteeBtn.addEventListener('click', submitAllNotesToGitee);
        console.log('已绑定笔记提交按钮：', submitNoteToGiteeBtn);
    }

    const viewGiteeHistoryBtn = document.getElementById('view-gitee-history-btn');
    if (viewGiteeHistoryBtn) {
        viewGiteeHistoryBtn.addEventListener('click', loadGiteeHistory);
        console.log('已绑定查看历史按钮：', viewGiteeHistoryBtn);
    }

    const loadGiteeHistoryBtn = document.getElementById('load-gitee-history-btn');
    if (loadGiteeHistoryBtn) {
        loadGiteeHistoryBtn.addEventListener('click', loadGiteeHistory);
        console.log('已绑定加载历史按钮：', loadGiteeHistoryBtn);
    }

    console.log('事件绑定完成！');
}

/**
 * 显示欢迎消息函数
 * 功能：在控制台显示欢迎消息
 * 说明：这个函数只是为了演示，实际应用中可能不需要
 */
function showWelcomeMessage() {
    const welcomeMessages = [
        '欢迎使用简单小工具！',
        '这是一个为初学者设计的自用小工具。',
        '代码简单易懂，适合学习。',
        '祝您使用愉快！'
    ];

    console.log('='.repeat(50));
    welcomeMessages.forEach(function(message) {
        console.log('💡 ' + message);
    });
    console.log('='.repeat(50));
}

/**
 * 初始化代码编辑器函数
 * 功能：初始化代码编辑器区域
 * 说明：这个函数设置代码编辑器的基本功能
 */
function initCodeEditor() {
    const codeEditor = document.getElementById('code-editor');
    const codeContent = document.getElementById('content'); // 代码内容文本框

    if (codeContent) {
        console.log('找到代码编辑器，正在初始化...');

        // 1. 自动调整高度
        codeContent.addEventListener('input', function() {
            // 根据行数调整高度
            const lines = codeContent.value.split('\n').length;
            codeContent.rows = Math.max(15, Math.min(40, lines + 5));
        });

        // 2. Tab键支持（插入4个空格而不是跳转到下一个元素）
        codeContent.addEventListener('keydown', function(event) {
            if (event.key === 'Tab') {
                event.preventDefault(); // 阻止默认的Tab行为

                // 获取当前光标位置
                const start = this.selectionStart;
                const end = this.selectionEnd;

                // 在光标位置插入4个空格
                this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);

                // 移动光标到插入位置后
                this.selectionStart = this.selectionEnd = start + 4;
            }
        });

        // 3. 自动保存草稿（可选功能）
        // 在实际应用中，可以添加自动保存功能
        // 这里只是一个示例
        let saveTimer;
        codeContent.addEventListener('input', function() {
            // 清除之前的计时器
            if (saveTimer) {
                clearTimeout(saveTimer);
            }

            // 设置新的计时器（5秒后保存）
            saveTimer = setTimeout(function() {
                console.log('代码已更改，可以添加自动保存功能');
            }, 5000);
        });

        console.log('代码编辑器初始化完成');
    } else if (codeEditor) {
        console.log('找到代码编辑器元素，但可能不是textarea');
    } else {
        console.log('未找到代码编辑器元素');
    }
}

/**
 * 初始化Markdown编辑器函数
 * 功能：初始化Markdown编辑器区域
 * 说明：这个函数设置Markdown编辑器的基本功能
 */
function initMarkdownEditor() {
    const markdownEditor = document.getElementById('markdown-editor');
    const previewArea = document.getElementById('markdown-preview');

    if (markdownEditor) {
        console.log('找到Markdown编辑器，正在初始化...');

        // 1. 自动调整高度
        markdownEditor.addEventListener('input', function() {
            // 根据行数调整高度
            const lines = markdownEditor.value.split('\n').length;
            markdownEditor.rows = Math.max(15, Math.min(40, lines + 5));

            // 更新预览
            updateMarkdownPreview();
        });

        // 2. Tab键支持（插入4个空格而不是跳转到下一个元素）
        markdownEditor.addEventListener('keydown', function(event) {
            if (event.key === 'Tab') {
                event.preventDefault(); // 阻止默认的Tab行为

                // 获取当前光标位置
                const start = this.selectionStart;
                const end = this.selectionEnd;

                // 在光标位置插入4个空格
                this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);

                // 移动光标到插入位置后
                this.selectionStart = this.selectionEnd = start + 4;

                // 更新预览
                updateMarkdownPreview();
            }
        });

        // 3. 实时预览（输入时更新）
        let previewTimer;
        markdownEditor.addEventListener('input', function() {
            // 清除之前的计时器
            if (previewTimer) {
                clearTimeout(previewTimer);
            }

            // 设置新的计时器（防抖，500毫秒后更新）
            previewTimer = setTimeout(updateMarkdownPreview, 500);
        });

        // 4. 初始更新预览
        updateMarkdownPreview();

        console.log('Markdown编辑器初始化完成');
    } else if (previewArea) {
        console.log('找到预览区域，但未找到编辑器');
    } else {
        console.log('未找到Markdown编辑器元素');
    }
}

/**
 * 保存代码函数
 * 功能：保存代码到服务器
 * 说明：这个函数处理代码保存逻辑
 */
function saveCode(event) {
    console.log('保存代码函数被调用');

    // 如果事件存在，阻止默认行为（除非我们想要手动控制）
    if (event) {
        event.preventDefault();
    }

    // 获取表单元素
    const form = event ? event.target.closest('form') : document.querySelector('form[action*="save_code"]');

    if (!form) {
        console.error('找不到保存代码的表单');
        alert('保存失败：找不到表单');
        return;
    }

    // 获取表单数据
    const formData = new FormData(form);
    const title = formData.get('title') || '';
    const content = formData.get('content') || '';

    // 验证输入
    if (!title.trim()) {
        alert('请输入代码标题！');
        const titleInput = form.querySelector('input[name="title"]');
        if (titleInput) titleInput.focus();
        return;
    }

    if (!content.trim()) {
        alert('请输入代码内容！');
        const contentInput = form.querySelector('textarea[name="content"]');
        if (contentInput) contentInput.focus();
        return;
    }

    // 显示保存提示
    console.log('正在保存代码...');

    // 在实际应用中，这里可以添加AJAX提交
    // 但现在我们直接提交表单
    form.submit();
}

/**
 * 保存笔记函数
 * 功能：保存笔记到服务器
 * 说明：这个函数处理笔记保存逻辑
 */
function saveDocument(event) {
    console.log('保存笔记函数被调用');

    // 如果事件存在，阻止默认行为（除非我们想要手动控制）
    if (event) {
        event.preventDefault();
    }

    // 获取表单元素
    const form = event ? event.target.closest('form') : document.querySelector('form[action*="save_document"]');

    if (!form) {
        console.error('找不到保存笔记的表单');
        alert('保存失败：找不到表单');
        return;
    }

    // 获取表单数据
    const formData = new FormData(form);
    const title = formData.get('title') || '';
    const content = formData.get('content') || '';

    // 验证输入
    if (!title.trim()) {
        alert('请输入笔记标题！');
        const titleInput = form.querySelector('input[name="title"]');
        if (titleInput) titleInput.focus();
        return;
    }

    if (!content.trim()) {
        alert('请输入笔记内容！');
        const contentInput = form.querySelector('textarea[name="content"]');
        if (contentInput) contentInput.focus();
        return;
    }

    // 显示保存提示
    console.log('正在保存笔记...');
    showMessage('正在保存笔记...', 'info');

    // 在实际应用中，这里可以添加AJAX提交
    // 但现在我们直接提交表单
    form.submit();
}

/**
 * 格式化代码函数
 * 功能：格式化代码（调整缩进、空格等）
 * 说明：这个函数格式化代码内容
 */
function formatCode(event) {
    console.log('格式化代码函数被调用');

    // 阻止事件冒泡
    if (event) {
        event.stopPropagation();
    }

    // 查找代码文本区域
    const codeTextarea = event ? event.target.closest('form').querySelector('textarea[name="content"]')
                               : document.querySelector('textarea[name="content"]');

    if (!codeTextarea) {
        console.error('找不到代码文本区域');
        alert('格式化失败：找不到代码编辑器');
        return;
    }

    // 获取当前代码
    let code = codeTextarea.value;

    // 使用simpleFormatCode函数格式化代码
    const formattedCode = simpleFormatCode(code);

    // 更新文本框内容
    codeTextarea.value = formattedCode;

    // 显示成功消息
    console.log('代码格式化完成');

    // 可选：显示提示（但可能会干扰用户体验）
    // showMessage('代码已格式化', 'success');
}

/**
 * 导入文件函数（模块6实现）
 * 功能：从本地文件导入代码或笔记
 * 说明：这个功能支持多种文件格式，自动识别并导入
 */
function importFile(event) {
    console.log('导入文件函数被调用');

    // 阻止事件冒泡
    if (event) {
        event.stopPropagation();
    }

    // 创建文件选择器
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.py,.js,.html,.css,.java,.cpp,.c,.sql,.sh,.bash,.md,.txt';

    // 当文件被选择时
    fileInput.onchange = function() {
        if (!fileInput.files || fileInput.files.length === 0) {
            console.log('没有选择文件');
            return;
        }

        const file = fileInput.files[0];
        console.log('选择了文件：' + file.name + ' (' + file.size + ' 字节)');

        // 检查文件大小（限制10MB）
        if (file.size > 10 * 1024 * 1024) {
            showMessage('文件太大，最大支持10MB', 'error');
            return;
        }

        // 读取文件内容
        const reader = new FileReader();
        reader.onload = function(e) {
            const content = e.target.result;
            const fileName = file.name;
            const fileExtension = fileName.split('.').pop().toLowerCase();

            // 显示处理中消息
            showMessage('正在处理文件...', 'info');

            // 调用后端API解析文件
            processUploadedFile(fileName, content);
        };
        reader.onerror = function() {
            showMessage('文件读取失败', 'error');
        };
        reader.readAsText(file);
    };

    // 触发文件选择
    fileInput.click();
}

/**
 * 处理上传的文件
 * 功能：调用后端API处理文件内容
 * 参数：fileName-文件名, content-文件内容
 */
function processUploadedFile(fileName, content) {
    // 使用FormData上传文件
    const formData = new FormData();
    const blob = new Blob([content], { type: 'text/plain' });
    formData.append('file', blob, fileName);

    // 调用后端API
    fetch('/api/file/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('文件处理成功：', data);
            handleImportedContent(data, fileName);
        } else {
            showMessage('文件处理失败：' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('文件上传失败：', error);
        showMessage('文件上传失败：' + error.message, 'error');
    });
}

/**
 * 处理导入的内容
 * 功能：根据文件类型跳转到相应页面并填充内容
 * 参数：fileData-文件数据, fileName-文件名
 */
function handleImportedContent(fileData, fileName) {
    const fileType = fileData.file_type;

    // 从文件名提取名称（不含扩展名）
    const title = fileName.replace(/\.[^/.]+$/, '');

    if (fileType === 'markdown') {
        // 跳转到笔记编辑器
        const url = '/markdown_editor?' +
            'title=' + encodeURIComponent(title) +
            '&content=' + encodeURIComponent(fileData.content);
        window.location.href = url;
    } else {
        // 跳转到代码编辑器
        const url = '/code_editor?' +
            'title=' + encodeURIComponent(title) +
            'code=' + encodeURIComponent(fileData.content) +
            '&language=' + encodeURIComponent(fileData.programming_language);
        window.location.href = url;
    }
}

/**
 * 导出文件函数（模块6实现）
 * 功能：将代码或笔记导出为本地文件
 * 说明：这个功能根据当前页面类型导出相应内容
 */
function exportFile(event) {
    console.log('导出文件函数被调用');

    // 阻止事件冒泡
    if (event) {
        event.stopPropagation();
    }

    // 检查当前页面类型
    const codeEditor = document.getElementById('code-editor');
    const markdownEditor = document.getElementById('markdown-editor');

    if (codeEditor) {
        // 在代码编辑器页面
        exportCurrentCode();
    } else if (markdownEditor) {
        // 在笔记编辑器页面
        exportCurrentDocument();
    } else {
        // 在其他页面
        showMessage('请先进入代码编辑器或笔记编辑器', 'info');
    }
}

/**
 * 导出当前代码
 * 功能：将当前编辑器中的代码导出为文件
 */
function exportCurrentCode() {
    // 获取代码内容和标题
    const codeEditor = document.getElementById('code-editor');
    const titleInput = document.getElementById('code-title');
    const languageSelect = document.getElementById('code-language');

    if (!codeEditor) {
        showMessage('找不到代码编辑器', 'error');
        return;
    }

    const code = codeEditor.value;
    const title = titleInput ? titleInput.value : 'untitled';
    const language = languageSelect ? languageSelect.value : 'python';

    if (!code.trim()) {
        showMessage('代码内容为空', 'info');
        return;
    }

    // 获取文件扩展名
    const extension = getFileExtension(language);
    const fileName = title + '.' + extension;

    // 下载文件
    downloadFile(code, fileName);
    showMessage('代码已导出：' + fileName, 'success');
}

/**
 * 导出当前笔记
 * 功能：将当前编辑器中的笔记导出为文件
 */
function exportCurrentDocument() {
    // 获取笔记内容和标题
    const markdownEditor = document.getElementById('markdown-editor');
    const titleInput = document.getElementById('document-title');

    if (!markdownEditor) {
        showMessage('找不到笔记编辑器', 'error');
        return;
    }

    const content = markdownEditor.value;
    const title = titleInput ? titleInput.value : 'untitled';

    if (!content.trim()) {
        showMessage('笔记内容为空', 'info');
        return;
    }

    // 生成文件名
    const fileName = title + '.md';

    // 下载文件
    downloadFile(content, fileName);
    showMessage('笔记已导出：' + fileName, 'success');
}

/**
 * 获取文件扩展名
 * 功能：根据编程语言返回对应的文件扩展名
 * 参数：language-编程语言
 * 返回值：文件扩展名
 */
function getFileExtension(language) {
    const extensions = {
        'python': 'py',
        'py': 'py',
        'javascript': 'js',
        'js': 'js',
        'html': 'html',
        'htm': 'html',
        'css': 'css',
        'java': 'java',
        'cpp': 'cpp',
        'c': 'c',
        'sql': 'sql',
        'sh': 'sh',
        'bash': 'sh',
        'markdown': 'md',
        'md': 'md',
        'text': 'txt'
    };

    return extensions[language.toLowerCase()] || 'txt';
}

/**
 * 切换Markdown预览函数
 * 功能：在Markdown编辑和预览模式之间切换
 * 说明：这个函数切换编辑器视图（编辑/预览/分屏）
 */
function toggleMarkdownPreview(event) {
    console.log('切换Markdown预览函数被调用');

    // 阻止事件冒泡
    if (event) {
        event.stopPropagation();
    }

    const editor = document.getElementById('markdown-editor');
    const preview = document.getElementById('markdown-preview');
    const container = editor ? editor.parentElement : null;

    if (!editor || !preview || !container) {
        console.error('找不到编辑器或预览区域');
        return;
    }

    // 获取当前显示状态
    const editorVisible = editor.style.display !== 'none';
    const previewVisible = preview.style.display !== 'none';

    // 切换模式：分屏 → 纯编辑 → 纯预览 → 分屏
    if (editorVisible && previewVisible) {
        // 当前是分屏模式，切换到纯编辑模式
        editor.style.flex = '1 1 100%';
        preview.style.display = 'none';
        console.log('切换到纯编辑模式');
        showMessage('已切换到编辑模式', 'info');
    } else if (editorVisible && !previewVisible) {
        // 当前是纯编辑模式，切换到纯预览模式
        editor.style.display = 'none';
        preview.style.display = 'block';
        preview.style.flex = '1 1 100%';
        console.log('切换到纯预览模式');
        showMessage('已切换到预览模式', 'info');
    } else {
        // 当前是纯预览模式，切换回分屏模式
        editor.style.display = 'block';
        preview.style.display = 'block';
        editor.style.flex = '1';
        preview.style.flex = '1';
        console.log('切换到分屏模式');
        showMessage('已切换到分屏模式', 'info');
    }

    // 更新预览内容
    updateMarkdownPreview();
}

/**
 * 更新Markdown预览函数
 * 功能：将Markdown转换为HTML并显示在预览区域
 * 说明：这个函数使用simpleParseMarkdown函数进行转换
 */
function updateMarkdownPreview() {
    const editor = document.getElementById('markdown-editor');
    const preview = document.getElementById('markdown-preview');

    if (!editor || !preview) {
        console.error('找不到编辑器或预览区域');
        return;
    }

    // 获取Markdown内容
    const markdown = editor.value;

    // 使用simpleParseMarkdown函数转换为HTML
    const html = simpleParseMarkdown(markdown);

    // 更新预览区域
    preview.innerHTML = html;

    console.log('Markdown预览已更新');
}

/**
 * 显示消息函数（增强版）
 * 功能：在页面上显示临时消息
 * 参数：
 *   message - 消息内容
 *   type - 消息类型（success, error, info, warning）
 *   duration - 显示时长（毫秒），默认3000ms
 * 说明：这是一个通用的消息显示函数，支持关闭按钮和不同显示时长
 */
function showMessage(message, type, duration) {
    // 设置默认显示时长
    if (duration === undefined) {
        // 不同类型使用不同的默认时长
        switch(type) {
            case 'error':
                duration = 5000;  // 错误消息显示更长时间
                break;
            case 'warning':
                duration = 4000;  // 警告消息
                break;
            default:
                duration = 3000;  // 成功和信息消息
        }
    }

    // 创建消息容器
    const messageContainer = document.createElement('div');
    messageContainer.className = 'message message-' + type;
    messageContainer.style.cssText = `
        background: ${getTypeColor(type)};
        color: white;
        padding: 12px 20px;
        margin: 10px 0;
        border-radius: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        animation: slideIn 0.3s ease-out;
    `;

    // 创建消息文本
    const messageText = document.createElement('span');
    messageText.textContent = message;

    // 创建关闭按钮
    const closeButton = document.createElement('button');
    closeButton.textContent = '×';
    closeButton.style.cssText = `
        background: none;
        border: none;
        color: white;
        font-size: 20px;
        cursor: pointer;
        padding: 0 5px;
        margin-left: 10px;
    `;
    closeButton.onclick = function() {
        removeMessage(messageContainer);
    };

    // 组装消息元素
    messageContainer.appendChild(messageText);
    messageContainer.appendChild(closeButton);

    // 将消息添加到页面顶部
    const mainElement = document.querySelector('.main .container');
    if (mainElement) {
        // 检查是否已有消息容器
        let messagesContainer = document.getElementById('messages-container');
        if (!messagesContainer) {
            // 创建消息容器
            messagesContainer = document.createElement('div');
            messagesContainer.id = 'messages-container';
            messagesContainer.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
            document.body.appendChild(messagesContainer);
        }
        messagesContainer.appendChild(messageContainer);

        // 自动移除消息
        const timeoutId = setTimeout(function() {
            removeMessage(messageContainer);
        }, duration);

        // 鼠标悬停时暂停自动移除
        messageContainer.onmouseenter = function() {
            clearTimeout(timeoutId);
        };
        messageContainer.onmouseleave = function() {
            setTimeout(function() {
                removeMessage(messageContainer);
            }, duration);
        };
    }
}

/**
 * 获取消息类型对应的颜色
 */
function getTypeColor(type) {
    const colors = {
        'success': '#2ecc71',
        'error': '#e74c3c',
        'info': '#3498db',
        'warning': '#f39c12'
    };
    return colors[type] || '#3498db';
}

/**
 * 移除消息
 */
function removeMessage(messageElement) {
    if (messageElement && messageElement.parentNode) {
        messageElement.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(function() {
            messageElement.remove();
            // 如果消息容器为空，也移除它
            const messagesContainer = document.getElementById('messages-container');
            if (messagesContainer && messagesContainer.children.length === 0) {
                messagesContainer.remove();
            }
        }, 300);
    }
}

// 添加动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

/**
 * 简单的代码格式化函数（基础版本）
 * 功能：对代码进行简单的格式化处理
 * 参数：code-要格式化的代码
 * 返回值：格式化后的代码
 * 说明：这是一个非常简单的格式化函数，只处理基本缩进
 */
function simpleFormatCode(code) {
    console.log('执行简单代码格式化...');

    // 将制表符替换为4个空格
    let formattedCode = code.replace(/\t/g, '    ');

    // 移除行尾的空格
    formattedCode = formattedCode.replace(/[ \t]+$/gm, '');

    // 确保文件末尾有换行符
    if (!formattedCode.endsWith('\n')) {
        formattedCode += '\n';
    }

    console.log('代码格式化完成');
    return formattedCode;
}

/**
 * 简单的Markdown解析函数（基础版本）
 * 功能：将Markdown转换为HTML
 * 参数：markdown-Markdown文本
 * 返回值：HTML文本
 * 说明：这是一个非常简单的解析函数，只处理基本语法
 */
function simpleParseMarkdown(markdown) {
    console.log('执行简单Markdown解析...');

    let html = markdown;

    // 处理标题（# 标题）
    html = html.replace(/^# (.*$)/gm, '<h1>$1</h1>');
    html = html.replace(/^## (.*$)/gm, '<h2>$1</h2>');
    html = html.replace(/^### (.*$)/gm, '<h3>$1</h3>');

    // 处理粗体（**粗体**）
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // 处理斜体（*斜体*）
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // 处理代码块（```代码```）
    html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');

    // 处理内联代码（`代码`）
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // 处理换行（两个空格加换行）
    html = html.replace(/  \n/g, '<br>');

    // 处理段落（空行分隔）
    html = html.replace(/\n\n/g, '</p><p>');
    html = '<p>' + html + '</p>';

    console.log('Markdown解析完成');
    return html;
}

/**
 * 下载文件函数
 * 功能：将文本内容下载为文件
 * 参数：content-文件内容, filename-文件名
 * 说明：这是一个通用的文件下载函数
 */
function downloadFile(content, filename) {
    // 创建Blob对象
    const blob = new Blob([content], { type: 'text/plain' });

    // 创建下载链接
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;

    // 触发下载
    document.body.appendChild(a);
    a.click();

    // 清理
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    console.log('文件下载完成：' + filename);
}

/**
 * 读取文件函数
 * 功能：读取用户选择的文件
 * 参数：fileInput-文件输入元素, callback-回调函数
 * 说明：这是一个通用的文件读取函数
 */
function readFile(fileInput, callback) {
    // 检查是否选择了文件
    if (!fileInput.files || fileInput.files.length === 0) {
        console.log('没有选择文件');
        return;
    }

    // 获取第一个文件
    const file = fileInput.files[0];

    // 创建FileReader对象
    const reader = new FileReader();

    // 文件读取完成时的回调函数
    reader.onload = function(e) {
        const content = e.target.result;
        console.log('文件读取完成：' + file.name);
        callback(content, file.name);
    };

    // 读取文件内容
    reader.readAsText(file);
}

// ============================================
// Gitee集成功能
// ============================================

/**
 * 初始化Gitee页面函数
 * 功能：初始化Gitee页面，加载用户配置
 * 说明：这个函数在Gitee页面加载时调用
 */
function initGiteePage() {
    console.log('正在初始化Gitee页面...');

    // 检查是否在Gitee页面
    const giteeForm = document.getElementById('gitee-config-form');
    if (!giteeForm) {
        console.log('不在Gitee页面，跳过初始化');
        return;
    }

    // 加载用户配置
    loadGiteeConfig();

    console.log('Gitee页面初始化完成！');
}

/**
 * 加载Gitee配置函数
 * 功能：从服务器获取用户的Gitee配置
 * 说明：这个函数在页面加载时调用，用于填充表单
 */
function loadGiteeConfig() {
    console.log('正在加载Gitee配置...');

    // 发送AJAX请求获取配置
    fetch('/gitee/get_config')
        .then(response => {
            if (!response.ok) {
                throw new Error('网络响应错误：' + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data.success && data.config) {
                // 填充表单
                document.getElementById('gitee-access-token').value = data.config.access_token;
                document.getElementById('gitee-repo-url').value = data.config.repo_url;
                showGiteeMessage('success', 'Gitee配置已加载');
            } else {
                // 没有配置或加载失败
                console.log('未找到Gitee配置：', data.message || '未知错误');
            }
        })
        .catch(error => {
            console.error('加载Gitee配置失败：', error);
            showGiteeMessage('error', '加载配置失败：' + error.message);
        });
}

/**
 * 保存Gitee配置函数
 * 功能：保存用户的Gitee配置
 * 说明：这个函数处理配置表单的提交
 */
function saveGiteeConfig() {
    console.log('正在保存Gitee配置...');

    // 获取表单数据
    const accessToken = document.getElementById('gitee-access-token').value.trim();
    const repoUrl = document.getElementById('gitee-repo-url').value.trim();

    // 验证输入
    if (!accessToken) {
        showGiteeMessage('error', 'Gitee访问令牌不能为空！');
        return;
    }
    if (!repoUrl) {
        showGiteeMessage('error', '仓库地址不能为空！');
        return;
    }

    // 显示加载状态
    const saveBtn = document.getElementById('save-gitee-config-btn');
    const originalText = saveBtn.textContent;
    saveBtn.textContent = '正在保存...';
    saveBtn.disabled = true;

    // 发送AJAX请求保存配置
    const formData = new FormData();
    formData.append('access_token', accessToken);
    formData.append('repo_url', repoUrl);

    fetch('/gitee/save_config', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('保存失败：' + response.status);
        }
        return response.text();
    })
    .then(result => {
        showGiteeMessage('success', result);
        console.log('Gitee配置保存成功：', result);
    })
    .catch(error => {
        showGiteeMessage('error', '保存配置失败：' + error.message);
        console.error('保存Gitee配置失败：', error);
    })
    .finally(() => {
        // 恢复按钮状态
        saveBtn.textContent = originalText;
        saveBtn.disabled = false;
    });
}

/**
 * 测试Gitee连接函数
 * 功能：测试Gitee连接是否正常
 * 说明：验证访问令牌和仓库访问权限
 */
function testGiteeConnection() {
    console.log('正在测试Gitee连接...');

    // 获取表单数据
    const accessToken = document.getElementById('gitee-access-token').value.trim();
    const repoUrl = document.getElementById('gitee-repo-url').value.trim();

    // 验证输入
    if (!accessToken) {
        showGiteeMessage('error', 'Gitee访问令牌不能为空！');
        return;
    }
    if (!repoUrl) {
        showGiteeMessage('error', '仓库地址不能为空！');
        return;
    }

    // 显示加载状态
    const testBtn = document.getElementById('test-gitee-connection-btn');
    const originalText = testBtn.textContent;
    testBtn.textContent = '正在测试...';
    testBtn.disabled = true;

    // 发送AJAX请求测试连接
    const formData = new FormData();
    formData.append('access_token', accessToken);
    formData.append('repo_url', repoUrl);

    fetch('/gitee/test_connection', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showGiteeMessage('success', 'Gitee连接测试成功！令牌和仓库访问权限验证通过。');
        } else {
            let errorMessage = 'Gitee连接测试失败：';
            if (data.errors && data.errors.length > 0) {
                errorMessage += data.errors.join('；');
            } else if (data.message) {
                errorMessage += data.message;
            }
            showGiteeMessage('error', errorMessage);
        }
    })
    .catch(error => {
        showGiteeMessage('error', '测试连接失败：' + error.message);
        console.error('测试Gitee连接失败：', error);
    })
    .finally(() => {
        // 恢复按钮状态
        testBtn.textContent = originalText;
        testBtn.disabled = false;
    });
}

/**
 * 提交所有代码到Gitee函数
 * 功能：提交所有代码片段到Gitee
 * 说明：这个函数批量提交用户的所有代码片段
 */
function submitAllCodeToGitee() {
    console.log('正在提交所有代码到Gitee...');

    // 显示确认对话框
    const confirmSubmit = confirm('您确定要提交所有代码片段到Gitee吗？\n\n提交前请确保：\n1. Gitee配置已正确设置\n2. 仓库地址和访问令牌有效\n3. 网络连接正常\n\n点击"确定"开始提交。');
    if (!confirmSubmit) {
        console.log('用户取消了代码提交');
        return;
    }

    // 获取提交消息
    const commitMessage = prompt('请输入提交消息：', `提交代码片段 - ${new Date().toLocaleString()}`);
    if (!commitMessage) {
        console.log('用户取消了提交消息输入');
        return;
    }

    // 显示提交状态
    const statusElement = document.getElementById('code-submit-status');
    if (statusElement) {
        statusElement.innerHTML = '<div class="message-info">正在准备提交...</div>';
        statusElement.style.display = 'block';
    }

    // 显示进度条
    updateGiteeProgress('code', 0, 1);

    // 发送AJAX请求提交代码
    const formData = new FormData();
    formData.append('commit_message', commitMessage);

    fetch('/gitee/submit/code', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('代码提交结果：', data);

        // 更新进度条
        updateGiteeProgress('code', data.success_count || 0, data.total || 1);

        if (data.success) {
            // 提交成功（至少部分成功）
            let message = `提交完成！成功 ${data.success_count} 个，失败 ${data.error_count} 个。`;
            if (data.error_count > 0) {
                message += ' 失败的项目请查看控制台日志。';
            }
            showGiteeMessage('success', message);

            // 更新状态显示
            if (statusElement) {
                statusElement.innerHTML = `<div class="message-success">${message}</div>`;
            }

            // 显示详细结果（可选）
            if (data.results && data.results.length > 0) {
                console.log('详细提交结果：', data.results);
            }
        } else {
            // 提交失败
            showGiteeMessage('error', data.message || '提交代码失败');
            if (statusElement) {
                statusElement.innerHTML = `<div class="message-error">${data.message || '提交代码失败'}</div>`;
            }
        }
    })
    .catch(error => {
        console.error('提交代码时发生错误：', error);
        showGiteeMessage('error', '提交失败：' + error.message);
        if (statusElement) {
            statusElement.innerHTML = `<div class="message-error">提交失败：${error.message}</div>`;
        }
    });
}

/**
 * 提交所有笔记到Gitee函数
 * 功能：提交所有笔记到Gitee
 * 说明：这个函数批量提交用户的所有笔记
 */
function submitAllNotesToGitee() {
    console.log('正在提交所有笔记到Gitee...');

    // 显示确认对话框
    const confirmSubmit = confirm('您确定要提交所有笔记到Gitee吗？\n\n提交前请确保：\n1. Gitee配置已正确设置\n2. 仓库地址和访问令牌有效\n3. 网络连接正常\n\n点击"确定"开始提交。');
    if (!confirmSubmit) {
        console.log('用户取消了笔记提交');
        return;
    }

    // 获取提交消息
    const commitMessage = prompt('请输入提交消息：', `提交笔记 - ${new Date().toLocaleString()}`);
    if (!commitMessage) {
        console.log('用户取消了提交消息输入');
        return;
    }

    // 显示提交状态
    const statusElement = document.getElementById('note-submit-status');
    if (statusElement) {
        statusElement.innerHTML = '<div class="message-info">正在准备提交...</div>';
        statusElement.style.display = 'block';
    }

    // 显示进度条
    updateGiteeProgress('note', 0, 1);

    // 发送AJAX请求提交笔记
    const formData = new FormData();
    formData.append('commit_message', commitMessage);

    fetch('/gitee/submit/note', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('笔记提交结果：', data);

        // 更新进度条
        updateGiteeProgress('note', data.success_count || 0, data.total || 1);

        if (data.success) {
            // 提交成功（至少部分成功）
            let message = `提交完成！成功 ${data.success_count} 个，失败 ${data.error_count} 个。`;
            if (data.error_count > 0) {
                message += ' 失败的项目请查看控制台日志。';
            }
            showGiteeMessage('success', message);

            // 更新状态显示
            if (statusElement) {
                statusElement.innerHTML = `<div class="message-success">${message}</div>`;
            }

            // 显示详细结果（可选）
            if (data.results && data.results.length > 0) {
                console.log('详细提交结果：', data.results);
            }
        } else {
            // 提交失败
            showGiteeMessage('error', data.message || '提交笔记失败');
            if (statusElement) {
                statusElement.innerHTML = `<div class="message-error">${data.message || '提交笔记失败'}</div>`;
            }
        }
    })
    .catch(error => {
        console.error('提交笔记时发生错误：', error);
        showGiteeMessage('error', '提交失败：' + error.message);
        if (statusElement) {
            statusElement.innerHTML = `<div class="message-error">提交失败：${error.message}</div>`;
        }
    });
}

/**
 * 加载Gitee历史记录函数
 * 功能：加载Gitee提交历史记录
 * 说明：这个函数从服务器获取提交历史并显示
 */
function loadGiteeHistory() {
    console.log('正在加载Gitee提交历史...');

    // 获取历史记录容器元素
    const historyList = document.getElementById('gitee-history-list');
    const historyEmpty = document.getElementById('gitee-history-empty');
    const historyContainer = document.getElementById('gitee-history-container');
    const historyFull = document.getElementById('gitee-history-full');

    // 如果正在Gitee页面，显示加载状态
    if (historyList) {
        historyList.innerHTML = '<div class="message-info">正在加载提交历史...</div>';
    }
    if (historyEmpty) {
        historyEmpty.style.display = 'none';
    }

    // 如果点击了查看历史按钮（在网格中），显示容器
    if (historyContainer && event && event.target.id === 'view-gitee-history-btn') {
        historyContainer.style.display = 'block';
    }

    // 发送AJAX请求获取历史记录
    fetch('/gitee/get_history?limit=20')
        .then(response => response.json())
        .then(data => {
            console.log('Gitee历史记录加载结果：', data);

            if (data.success && data.history && data.history.length > 0) {
                // 有历史记录，显示列表
                displayGiteeHistory(data.history);

                // 显示成功消息
                showGiteeMessage('success', `已加载 ${data.count} 条提交记录`);
            } else {
                // 没有历史记录或加载失败
                const message = data.message || '暂无提交记录';

                if (historyList) {
                    historyList.innerHTML = `<div class="message-info">${message}</div>`;
                }

                if (historyEmpty) {
                    historyEmpty.style.display = 'block';
                    historyEmpty.innerHTML = `<p>${message}</p>`;
                }

                if (!data.success) {
                    showGiteeMessage('error', message);
                }
            }
        })
        .catch(error => {
            console.error('加载Gitee历史记录失败：', error);
            showGiteeMessage('error', '加载历史记录失败：' + error.message);

            if (historyList) {
                historyList.innerHTML = `<div class="message-error">加载失败：${error.message}</div>`;
            }
        });
}

/**
 * 显示Gitee历史记录函数
 * 功能：在页面上显示Gitee提交历史记录
 * 参数：history-历史记录数组
 * 说明：这个函数将历史记录渲染为HTML表格
 */
function displayGiteeHistory(history) {
    console.log('正在显示Gitee历史记录：', history.length, '条记录');

    // 获取历史记录容器元素
    const historyList = document.getElementById('gitee-history-list');
    const historyEmpty = document.getElementById('gitee-history-empty');
    const historyContainer = document.getElementById('gitee-history-container');

    if (!historyList) {
        console.error('找不到历史记录列表容器');
        return;
    }

    // 如果没有历史记录
    if (!history || history.length === 0) {
        historyList.innerHTML = '<div class="message-info">暂无提交记录</div>';
        if (historyEmpty) {
            historyEmpty.style.display = 'block';
        }
        return;
    }

    // 创建历史记录表格
    let html = '<table class="history-table">';
    html += '<thead><tr>';
    html += '<th>提交类型</th>';
    html += '<th>项目数量</th>';
    html += '<th>提交消息</th>';
    html += '<th>提交时间</th>';
    html += '<th>状态</th>';
    html += '</tr></thead>';
    html += '<tbody>';

    // 添加每一行记录
    history.forEach(record => {
        const commitType = record.commit_type === 'code' ? '代码' : '笔记';
        const itemCount = record.item_count || 0;
        const commitMessage = record.commit_message || '无消息';
        const createdTime = record.created_at_formatted || record.created_at || '未知时间';
        const successStatus = record.success ? '成功' : '失败';
        const statusClass = record.success ? 'history-success' : 'history-error';

        html += '<tr>';
        html += `<td>${commitType}</td>`;
        html += `<td>${itemCount}</td>`;
        html += `<td title="${commitMessage}">${commitMessage.length > 30 ? commitMessage.substring(0, 30) + '...' : commitMessage}</td>`;
        html += `<td>${createdTime}</td>`;
        html += `<td class="${statusClass}">${successStatus}</td>`;
        html += '</tr>';
    });

    html += '</tbody></table>';

    // 更新容器内容
    historyList.innerHTML = html;

    // 隐藏"暂无记录"消息
    if (historyEmpty) {
        historyEmpty.style.display = 'none';
    }

    // 如果是在网格中查看历史，确保容器可见
    if (historyContainer) {
        historyContainer.style.display = 'block';
    }

    console.log('Gitee历史记录显示完成');
}

/**
 * 显示Gitee消息函数
 * 功能：在Gitee页面上显示消息
 * 参数：type-消息类型（success, error, info, warning）, text-消息文本
 * 说明：这个函数在Gitee配置区域显示消息
 */
function showGiteeMessage(type, text) {
    const messageElement = document.getElementById('gitee-config-message');
    if (!messageElement) {
        console.log('找不到Gitee消息元素，无法显示消息：', text);
        return;
    }

    // 设置消息内容和样式
    messageElement.textContent = text;
    messageElement.className = 'message-' + type;
    messageElement.style.display = 'block';

    // 5秒后自动隐藏消息
    setTimeout(() => {
        messageElement.style.display = 'none';
    }, 5000);
}

/**
 * 更新进度条函数
 * 功能：更新提交进度条
 * 参数：elementId-进度条元素ID, current-当前进度, total-总进度
 * 说明：这个函数更新进度条的显示
 */
function updateGiteeProgress(elementId, current, total) {
    // elementId可以是'code'或'note'
    const progressFill = document.getElementById(elementId + '-progress-fill');
    const progressText = document.getElementById(elementId + '-progress-text');
    const progressContainer = document.getElementById(elementId + '-submit-progress');

    if (!progressFill || !progressText || !progressContainer) {
        console.log('找不到进度条元素：', elementId);
        return;
    }

    // 计算百分比
    const percentage = total > 0 ? Math.round((current / total) * 100) : 0;

    // 更新进度条
    progressFill.style.width = percentage + '%';
    progressText.textContent = current + '/' + total;

    // 显示进度条容器
    progressContainer.style.display = 'block';
}

// 导出函数（如果需要）
// 这里列出所有可以外部调用的函数
window.CodeTool = {
    initPage: initPage,
    bindEvents: bindEvents,
    showMessage: showMessage,
    saveCode: saveCode,
    saveDocument: saveDocument,
    formatCode: formatCode,
    simpleFormatCode: simpleFormatCode,
    simpleParseMarkdown: simpleParseMarkdown,
    downloadFile: downloadFile,
    readFile: readFile,
    initCodeEditor: initCodeEditor,
    initMarkdownEditor: initMarkdownEditor,
    updateMarkdownPreview: updateMarkdownPreview,
    toggleMarkdownPreview: toggleMarkdownPreview,
    // Gitee相关函数
    initGiteePage: initGiteePage,
    saveGiteeConfig: saveGiteeConfig,
    testGiteeConnection: testGiteeConnection,
    submitAllCodeToGitee: submitAllCodeToGitee,
    submitAllNotesToGitee: submitAllNotesToGitee,
    loadGiteeHistory: loadGiteeHistory,
    showGiteeMessage: showGiteeMessage,
    updateGiteeProgress: updateGiteeProgress
};