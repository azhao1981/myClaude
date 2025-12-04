import functools
import time
import logging
import json
from typing import Any, Callable

# 建议根据项目实际情况修改 Logger 名称
logger = logging.getLogger("audit")

class SafeJSONEncoder(json.JSONEncoder):
    """防止日志中出现无法序列化的对象导致报错"""
    def default(self, obj):
        return str(obj)

def log_execution(op_name: str = None, log_args: bool = True, log_result: bool = True):
    """
    [Standardized Logging Decorator]
    自动记录：函数名、入参、出参、精确耗时(ms)、异常堆栈。
    
    Args:
        op_name: 业务操作名称 (可选)
        log_args: 是否打印入参 (涉及敏感数据可关)
        log_result: 是否打印结果 (结果过大可关)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 1. 准备上下文
            func_name = op_name or func.__name__
            start_pc = time.perf_counter() # 高精度计时器
            
            # 2. 记录入参 (Input)
            if log_args:
                try:
                    # 尝试序列化，如果失败则转字符串，避免日志炸库
                    args_repr = json.dumps(args, cls=SafeJSONEncoder, ensure_ascii=False)
                    kwargs_repr = json.dumps(kwargs, cls=SafeJSONEncoder, ensure_ascii=False)
                    logger.info(f"[{func_name}] START | Args: {args_repr} | Kwargs: {kwargs_repr}")
                except Exception:
                    logger.info(f"[{func_name}] START | Args: (serialization_failed)")
            else:
                 logger.info(f"[{func_name}] START")

            try:
                # 3. 执行核心逻辑
                result = func(*args, **kwargs)
                
                # 4. 记录结果 (Output) 与 耗时
                duration_ms = (time.perf_counter() - start_pc) * 1000
                if log_result:
                    try:
                        res_repr = json.dumps(result, cls=SafeJSONEncoder, ensure_ascii=False)
                        # 截断过长的日志，防止刷屏
                        if len(res_repr) > 1000: 
                            res_repr = res_repr[:1000] + "...(truncated)"
                        logger.info(f"[{func_name}] OK | Time: {duration_ms:.2f}ms | Result: {res_repr}")
                    except Exception:
                        logger.info(f"[{func_name}] OK | Time: {duration_ms:.2f}ms | Result: (serialization_failed)")
                else:
                    logger.info(f"[{func_name}] OK | Time: {duration_ms:.2f}ms")
                    
                return result
                
            except Exception as e:
                # 5. 异常记录 (Exception)
                duration_ms = (time.perf_counter() - start_pc) * 1000
                logger.exception(f"[{func_name}] FAIL | Time: {duration_ms:.2f}ms | Error: {str(e)}")
                raise e
        return wrapper
    return decorator