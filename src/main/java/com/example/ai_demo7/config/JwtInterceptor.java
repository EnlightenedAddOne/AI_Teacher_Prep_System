package com.example.ai_demo7.config;

import com.example.ai_demo7.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@Component
public class JwtInterceptor implements HandlerInterceptor {
    @Autowired
    private JwtUtil jwtUtil;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String token = request.getHeader("Authorization");
        if (token == null || !token.startsWith("Bearer ")) {
            response.sendError(401, "未提供有效的Token");
            return false;
        }

        token = token.substring(7);
        if (!jwtUtil.validateToken(token)) {
            response.sendError(401, "Token无效或已过期");
            return false;
        }

        // 将用户信息存入请求属性
        request.setAttribute("claims", jwtUtil.parseToken(token));
        return true;
    }
}