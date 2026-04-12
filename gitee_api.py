"""
Gitee API模块
功能：封装Gitee API调用，提供简单的接口
作者：大一学生助手
创建时间：2026-04-10

这个模块封装了Gitee API的调用，提供验证令牌、验证仓库访问、创建文件等功能。
所有API调用都使用requests库，错误处理简单明了。
代码设计保持简单，适合初学者学习。
"""

import requests
import json
import base64

class GiteeClient:
    """
    Gitee API客户端类
    功能：封装Gitee API调用，提供简单的接口
    说明：这个类封装了Gitee API的调用，包括验证令牌、验证仓库访问、创建文件等。
    """

    def __init__(self, access_token):
        """
        初始化Gitee客户端
        参数：access_token Gitee个人访问令牌
        说明：创建Gitee API客户端实例，设置基础URL。
        """
        self.access_token = access_token
        self.base_url = "https://gitee.com/api/v5"

    def verify_token(self):
        """
        验证访问令牌函数
        功能：验证Gitee访问令牌是否有效
        返回值：(是否成功, 错误信息)元组
              成功时返回(True, "")，失败时返回(False, 错误描述)
        说明：通过调用Gitee API的/user端点验证令牌。
        """
        try:
            # 调用Gitee API验证令牌
            # GET /api/v5/user 可以获取当前用户信息，用于验证令牌
            # Gitee API使用access_token查询参数进行认证
            url = f"{self.base_url}/user?access_token={self.access_token}"
            response = requests.get(url, timeout=10)

            # 检查响应状态码
            # 200表示成功，令牌有效
            if response.status_code == 200:
                print("Gitee令牌验证成功！")
                return True, ""
            else:
                # 其他状态码表示令牌无效或有错误
                error_msg = f"Gitee令牌验证失败：{response.status_code} - {response.text}"
                print(error_msg)
                # 尝试提取错误信息
                try:
                    error_json = response.json()
                    if 'message' in error_json:
                        error_detail = f"{response.status_code}: {error_json['message']}"
                    else:
                        error_detail = f"{response.status_code}: {response.text}"
                except:
                    error_detail = f"{response.status_code}: {response.text}"

                return False, error_detail

        except requests.exceptions.RequestException as e:
            # 网络错误或请求异常
            error_msg = f"验证Gitee令牌时发生错误：{e}"
            print(error_msg)
            return False, str(e)

    def parse_repo_url(self, repo_url):
        """
        解析仓库URL函数
        功能：从仓库URL中提取owner和repo名称
        参数：repo_url 仓库URL（例如：https://gitee.com/username/repo）
        返回值：包含owner和repo的字典，如果URL格式错误返回None
        说明：Gitee API需要owner和repo名称，这个函数从URL中提取它们。
        """
        try:
            # 移除协议前缀和末尾斜杠
            repo_url = repo_url.strip().rstrip('/')

            # 提取路径部分
            if repo_url.startswith('https://gitee.com/'):
                path = repo_url[19:]  # 移除"https://gitee.com/"
            elif repo_url.startswith('http://gitee.com/'):
                path = repo_url[18:]  # 移除"http://gitee.com/"
            else:
                print(f"仓库URL格式错误：{repo_url}")
                return None

            # 分割路径获取owner和repo
            parts = path.split('/')
            if len(parts) >= 2:
                owner = parts[0]
                repo = parts[1]
                return {"owner": owner, "repo": repo}
            else:
                print(f"仓库URL格式错误：{repo_url}")
                return None

        except Exception as e:
            print(f"解析仓库URL时发生错误：{e}")
            return None

    def verify_repo_access(self, repo_url):
        """
        验证仓库访问权限函数
        功能：验证用户是否有指定仓库的写入权限
        参数：repo_url 仓库URL
        返回值：(是否成功, 错误信息)元组
              成功时返回(True, "")，失败时返回(False, 错误描述)
        说明：通过调用Gitee API的/repos/{owner}/{repo}端点验证访问权限。
        """
        try:
            # 解析仓库URL
            repo_info = self.parse_repo_url(repo_url)
            if not repo_info:
                return False, "仓库URL格式错误"

            owner = repo_info["owner"]
            repo = repo_info["repo"]

            # 调用Gitee API获取仓库信息
            # GET /api/v5/repos/{owner}/{repo}
            # Gitee API使用access_token查询参数进行认证
            url = f"{self.base_url}/repos/{owner}/{repo}?access_token={self.access_token}"
            response = requests.get(url, timeout=10)

            # 检查响应状态码
            # 200表示成功，用户有仓库访问权限
            if response.status_code == 200:
                print(f"仓库访问验证成功：{owner}/{repo}")
                return True, ""
            else:
                error_msg = f"仓库访问验证失败：{response.status_code} - {response.text}"
                print(error_msg)
                # 尝试提取错误信息
                try:
                    error_json = response.json()
                    if 'message' in error_json:
                        error_detail = f"{response.status_code}: {error_json['message']}"
                    else:
                        error_detail = f"{response.status_code}: {response.text}"
                except:
                    error_detail = f"{response.status_code}: {response.text}"

                return False, error_detail

        except requests.exceptions.RequestException as e:
            # 网络错误或请求异常
            error_msg = f"验证仓库访问权限时发生错误：{e}"
            print(error_msg)
            return False, str(e)

    def create_or_update_file(self, repo_url, file_path, content, commit_message):
        """
        创建或更新文件函数
        功能：在Gitee仓库中创建或更新文件
        参数：
          repo_url 仓库URL
          file_path 文件路径（在仓库中的路径，如：code/python/hello.py）
          content 文件内容
          commit_message 提交消息
        返回值：如果成功返回包含文件信息的字典，失败返回None
        说明：这个函数先检查文件是否存在，如果存在则更新，否则创建新文件。
        """
        try:
            # 解析仓库URL
            repo_info = self.parse_repo_url(repo_url)
            if not repo_info:
                return None

            owner = repo_info["owner"]
            repo = repo_info["repo"]

            # 构建API URL
            api_url = f"{self.base_url}/repos/{owner}/{repo}/contents/{file_path}"

            # 准备请求数据
            # Gitee API要求content字段使用base64编码
            content_base64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            data = {
                "access_token": self.access_token,
                "content": content_base64,
                "message": commit_message
            }

            # 首先检查文件是否存在
            check_response = requests.get(
                f"{api_url}?access_token={self.access_token}",
                timeout=10
            )

            if check_response.status_code == 200:
                # 文件已存在，需要获取sha进行更新
                file_info = check_response.json()
                data["sha"] = file_info.get("sha")
                # 使用PUT请求更新文件
                response = requests.put(api_url, json=data, timeout=10)
                action = "更新"
            else:
                # 文件不存在，创建新文件
                # 使用POST请求创建文件
                response = requests.post(api_url, json=data, timeout=10)
                action = "创建"

            # 检查响应
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"文件{action}成功：{file_path}")
                return {
                    "success": True,
                    "action": action,
                    "file_path": file_path,
                    "html_url": result.get("content", {}).get("html_url", ""),
                    "sha": result.get("content", {}).get("sha", "")
                }
            else:
                print(f"文件{action}失败：{response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"API错误：{response.status_code}",
                    "message": response.text
                }

        except requests.exceptions.RequestException as e:
            # 网络错误或请求异常
            print(f"创建或更新文件时发生错误：{e}")
            return {
                "success": False,
                "error": "网络错误",
                "message": str(e)
            }

    def test_connection(self, repo_url):
        """
        测试连接函数
        功能：测试Gitee连接是否正常
        参数：repo_url 仓库URL
        返回值：包含测试结果的字典
        说明：这个函数同时测试令牌和仓库访问权限，返回详细的测试结果。
        """
        result = {
            "token_valid": False,
            "repo_access": False,
            "errors": []
        }

        # 测试令牌
        token_valid, error_detail = self.verify_token()
        if token_valid:
            result["token_valid"] = True
        else:
            error_msg = "Gitee访问令牌无效"
            if error_detail:
                error_msg += f"：{error_detail}"
            else:
                error_msg += "或网络连接失败"
            result["errors"].append(error_msg)

        # 测试仓库访问
        if result["token_valid"]:
            repo_access, error_detail = self.verify_repo_access(repo_url)
            if repo_access:
                result["repo_access"] = True
            else:
                error_msg = "无法访问指定仓库"
                if error_detail:
                    error_msg += f"：{error_detail}"
                else:
                    error_msg += "，请检查仓库地址和访问权限"
                result["errors"].append(error_msg)

        return result


# 测试代码
# 如果直接运行这个文件，会演示Gitee API的基本用法
if __name__ == '__main__':
    print("Gitee API模块测试")
    print("=" * 50)

    # 提示用户输入访问令牌（仅用于测试）
    access_token = input("请输入Gitee访问令牌（测试用）：").strip()
    repo_url = input("请输入仓库URL（例如：https://gitee.com/username/repo）：").strip()

    if not access_token or not repo_url:
        print("测试已取消：访问令牌和仓库URL不能为空")
    else:
        # 创建Gitee客户端
        client = GiteeClient(access_token)

        # 测试连接
        print("\n正在测试Gitee连接...")
        test_result = client.test_connection(repo_url)

        if test_result["token_valid"] and test_result["repo_access"]:
            print("✓ Gitee连接测试成功！")
            print(f"  令牌验证：{'成功' if test_result['token_valid'] else '失败'}")
            print(f"  仓库访问：{'成功' if test_result['repo_access'] else '失败'}")
        else:
            print("✗ Gitee连接测试失败：")
            for error in test_result["errors"]:
                print(f"  - {error}")