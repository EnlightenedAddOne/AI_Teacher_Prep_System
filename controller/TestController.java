package com.example.ai_teach_system.controller;

import com.example.ai_teach_system.service.SysUserService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;

@RestController
public class TestController {
    @Autowired
    SysUserService sysUserService;

    @GetMapping("/test")
    public Object test(){
        return sysUserService.list();
    }
}
