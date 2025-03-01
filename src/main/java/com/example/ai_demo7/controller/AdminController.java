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
            @RequestAttribute("claims") Claims claims,
            @RequestBody User newUser) {

        if (!"ADMIN".equals(claims.get("role"))) {
            return ResponseEntity.status(403).body("无权限操作");
        }

        if (!"TEACHER".equals(newUser.getRole()) && !"STUDENT".equals(newUser.getRole())) {
            return ResponseEntity.badRequest().body("角色必须为TEACHER或STUDENT");
        }
        if ("STUDENT".equals(newUser.getRole())) {
            // 如果指定了教师
            if (newUser.getCreatedBy() != null) {
                User teacher = userMapper.findByUsername(newUser.getCreatedBy());
                if (teacher == null || !"TEACHER".equals(teacher.getRole())) {
                    return ResponseEntity.badRequest().body("指定教师不存在或角色错误");
                }
            } else {
                // 默认创建者为管理员
                newUser.setCreatedBy(claims.getSubject());
            }
        } else {
            // 教师和管理员的created_by固定为管理员
            newUser.setCreatedBy(claims.getSubject());
        }

        newUser.setCreatedBy(claims.getSubject());

        if (userMapper.findByUsername(newUser.getUsername()) != null) {
            return ResponseEntity.badRequest().body("用户名已存在");
        }

        userMapper.insert(newUser);
        return ResponseEntity.ok("用户创建成功");
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
    @GetMapping("/admin/users")
    public ResponseEntity<?> getAllUsers(@RequestAttribute("claims") Claims claims) {
        if (!"ADMIN".equals(claims.get("role"))) {
            return ResponseEntity.status(403).body("无权限操作");
        }
        return ResponseEntity.ok(userMapper.findAll());
    }

    @PutMapping("/admin/assign-student")
    public ResponseEntity<?> assignStudentToTeacher(
            @RequestAttribute("claims") Claims claims,
            @RequestParam String studentUsername,
            @RequestParam String teacherUsername) {

        // 权限验证
        if (!"ADMIN".equals(claims.get("role"))) {
            return ResponseEntity.status(403).body("无权限操作");
        }

        // 验证学生信息
        User student = userMapper.findByUsername(studentUsername);
        if (student == null || !"STUDENT".equals(student.getRole())) {
            return ResponseEntity.badRequest().body("学生不存在或角色错误");
        }

        // 验证教师信息
        User teacher = userMapper.findByUsername(teacherUsername);
        if (teacher == null || !"TEACHER".equals(teacher.getRole())) {
            return ResponseEntity.badRequest().body("教师不存在或角色错误");
        }

        // 执行分配
        userMapper.updateCreatedBy(studentUsername, teacherUsername);
        return ResponseEntity.ok("学生分配成功");
    }
}