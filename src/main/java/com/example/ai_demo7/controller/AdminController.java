package com.example.ai_demo7.controller;

import com.example.ai_demo7.entity.User;
import com.example.ai_demo7.mapper.UserMapper;
import com.example.ai_demo7.util.JwtUtil;
import io.jsonwebtoken.Claims;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AdminController {
    @Autowired
    private UserMapper userMapper;
    @Autowired
    private JwtUtil jwtUtil;

    @PostMapping("/admin/create-user")
    public ResponseEntity<?> createUser(
            @RequestHeader("Authorization") String token,
            @RequestBody User newUser) {

        // 验证Token和权限
        Claims claims = jwtUtil.parseToken(token.replace("Bearer ", ""));
        if (!"ADMIN".equals(claims.get("role"))) {
            return ResponseEntity.status(403).body("无权限操作");
        }

        // 检查用户是否存在
        User existingUser = userMapper.findByUsername(newUser.getUsername());
        if (existingUser != null) {
            return ResponseEntity.badRequest().body("用户名已存在");
        }

        // 保存新用户
        userMapper.insert(newUser);
        return ResponseEntity.ok().body("用户创建成功");
    }
}