package com.example.ai_demo7.controller;

import com.example.ai_demo7.entity.User;
import com.example.ai_demo7.mapper.UserMapper;
import com.example.ai_demo7.util.JwtUtil;
import io.jsonwebtoken.Claims;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

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
    @DeleteMapping("/admin/delete-user/{username}")
    public ResponseEntity<?> deleteUser(
            @RequestAttribute("claims") Claims claims,  // 直接从请求属性获取已解析的claims
            @PathVariable String username) {

        // 验证管理员权限
        if (!"ADMIN".equals(claims.get("role"))) {
            return ResponseEntity.status(403).body("无权限操作");
        }

        // 检查用户是否存在
        User existingUser = userMapper.findByUsername(username);
        if (existingUser == null) {
            return ResponseEntity.badRequest().body("用户不存在");
        }

        // 执行删除
        userMapper.deleteByUsername(username);
        return ResponseEntity.ok().body("用户删除成功");
    }

    @PutMapping("/admin/update-user")
    public ResponseEntity<?> updateUser(
            @RequestAttribute("claims") Claims claims,
            @RequestBody User updatedUser) {

        // 验证管理员权限
        if (!"ADMIN".equals(claims.get("role"))) {
            return ResponseEntity.status(403).body("无权限操作");
        }

        // 检查目标用户是否存在
        User existingUser = userMapper.findByUsername(updatedUser.getUsername());
        if (existingUser == null) {
            return ResponseEntity.badRequest().body("用户不存在");
        }

        // 更新用户信息（保留原用户名）
        userMapper.updateByUsername(updatedUser);
        return ResponseEntity.ok().body("用户信息更新成功");
    }
}