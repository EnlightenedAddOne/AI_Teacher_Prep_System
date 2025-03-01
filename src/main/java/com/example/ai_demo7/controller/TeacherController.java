package com.example.ai_demo7.controller;

import com.example.ai_demo7.entity.User;
import com.example.ai_demo7.mapper.UserMapper;
import io.jsonwebtoken.Claims;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/teacher")
public class TeacherController {
    @Autowired
    private UserMapper userMapper;

    @PostMapping("/create-student")
    public ResponseEntity<?> createStudent(@RequestAttribute("claims") Claims claims,
                                           @RequestBody User student) {
        if (!"TEACHER".equals(claims.get("role"))) {
            return ResponseEntity.status(403).body("无权限操作");
        }

        student.setRole("STUDENT");
        student.setCreatedBy(claims.getSubject());

        if (userMapper.findByUsername(student.getUsername()) != null) {
            return ResponseEntity.badRequest().body("用户名已存在");
        }

        userMapper.insert(student);
        return ResponseEntity.ok("学生创建成功");
    }

    @GetMapping("/students")
    public ResponseEntity<?> getStudents(@RequestAttribute("claims") Claims claims) {
        List<User> students = userMapper.findByCreatedBy(claims.getSubject());
        return ResponseEntity.ok(students);
    }

    @DeleteMapping("/delete-student/{username}")
    public ResponseEntity<?> deleteStudent(@RequestAttribute("claims") Claims claims,
                                           @PathVariable String username) {
        User student = userMapper.findByUsername(username);
        if (student == null || !student.getCreatedBy().equals(claims.getSubject())) {
            return ResponseEntity.badRequest().body("学生不存在或无权操作");
        }

        userMapper.deleteByUsername(username);
        return ResponseEntity.ok("学生删除成功");
    }
}
