# Ağ bağlantı envanteri

9 Eylül 2026; KiCad netlist çıktısı. J1 referans çakışması için ana rapora bakınız.

| Ağ | Bağlanan pinler |
|---|---|
| +3.3V | C11.1 , C5.1 , C6.1 , C9.1 , J3.32 Pin_32_32, J3.33 Pin_33_33, J3.7 Pin_7_7, J3.8 Pin_8_8, Q1.1 G_1, Q2.1 G_1, R1.1 , R10.2 , R24.1 , R25.1 , R26.2 , R27.1 , R34.1 , R35.1 , R36.1 , R4.2 , R7.1 , U2.2 3V3_2, U3.6 VS_6, U4.7 VDD_7 |
| /MCU/RTC_INT | R24.2 , U2.27 GPIO2/ADC1_CH2_27, U4.2 ~{INT}_2 |
| /MCU/RTC_SCL | U2.7 MTDO/GPIO7_7 |
| /MCU/RTC_SDA | R26.1 , U2.6 MTCK/GPIO6/ADC1_CH6_6, U4.4 SDA_4 |
| /MCU/UART_RX | J1.2 2_2, U2.24 U0RXD/GPIO17_24 |
| /MCU/UART_TX | J1.1 1_1, U2.25 U0TXD/GPIO16_25 |
| /USB_PD_CONTROLLER/PD_GATE | Q3.1 G_1, Q4.1 G_1, R12.2 , TP5.1 1_1 |
| BACKLIGHT_3V0 | J3.38 Pin_38_38 |
| BL_SINK | R30.1 , R31.1 , R32.1 , R33.1  |
| ENCODER_A | R34.2 , SW3.1 A_1, U2.20 GPIO22_20 |
| ENCODER_B | R35.2 , SW3.3 B_3, U2.21 GPIO23_21 |
| ENCODER_SW | R36.2 , SW3.4 S1_4, U2.19 GPIO21_19 |
| GND | BT1.2 -_2, C1.2 , C10.2 , C11.2 , C2.2 , C3.2 , C4.2 , C5.2 , C6.2 , C7.1 , C8.2 , C9.2 , D1.2 A_2, J1.3 3_3, J1.A1 GND_A1, J1.A12 GND_A12, J1.B1 GND_B1, J1.B12 GND_B12, J1.SH SHIELD_SH, J3.1 Pin_1_1, J3.31 Pin_31_31, J3.39 Pin_39_39, Q6.2 S_2, R21.1 , R23.2 , R29.2 , R9.2 , SW1.1 1_1, SW2.1 1_1, SW3.2 C_2, SW3.5 S2_5, TH1.1 , U1.25 GND_25, U1.3 GND_3, U2.1 GND_1, U2.28 GND_28, U2.29 GND_29, U3.1 A1_1, U3.2 A0_2, U3.7 GND_7, U4.5 VSS_5, U5.3 GND_3 |
| INA_ALERT | R27.2 , U2.26 GPIO3/ADC1_CH3_26, U3.3 ~{Alert}_3 |
| Net-(BT1-+) | BT1.1 +_1, R22.2  |
| Net-(D1-K) | D1.1 K_1, R14.2  |
| Net-(J3-Pin_34) | J3.34 Pin_34_34, R33.2  |
| Net-(J3-Pin_35) | J3.35 Pin_35_35, R32.2  |
| Net-(J3-Pin_36) | J3.36 Pin_36_36, R31.2  |
| Net-(J3-Pin_37) | J3.37 Pin_37_37, R30.2  |
| Net-(Q3-S) | Q3.2 S_2, Q4.2 S_2 |
| Net-(Q6-G) | Q6.1 G_1, R28.2 , R29.1  |
| Net-(R15-Pad2) | R15.2 , TP9.1 1_1 |
| Net-(R16-Pad1) | R16.1 , TP10.1 1_1 |
| Net-(U1-IFB) | C2.1 , U1.15 IFB_15 |
| Net-(U1-LED) | R14.1 , U1.8 LED_8 |
| Net-(U1-OTP) | TH1.2 , U1.13 OTP_13 |
| Net-(U1-PWR_EN) | R12.1 , U1.23 PWR_EN_23 |
| Net-(U1-V18) | C1.1 , U1.12 V18_12 |
| Net-(U1-VOUT) | R13.1 , U1.22 VOUT_22 |
| Net-(U1-VSEL) | R21.2 , U1.11 VSEL_11 |
| Net-(U2-EN/CHIP_PU) | C7.2 , R1.2 , SW2.2 2_2, U2.3 EN/CHIP_PU_3 |
| Net-(U2-GPIO0/ADC1_CH0/XTAL_32K_P) | R16.2 , U2.8 GPIO0/ADC1_CH0/XTAL_32K_P_8 |
| Net-(U2-GPIO8) | R15.1 , U2.10 GPIO8_10 |
| Net-(U2-GPIO9) | R10.1 , SW1.2 2_2, U2.15 GPIO9_15 |
| Net-(U2-GPIO12/USB_D-) | R3.1 , U2.13 GPIO12/USB_D-_13 |
| Net-(U2-GPIO13/USB_D+) | R2.1 , U2.14 GPIO13/USB_D+_14 |
| Net-(U4-EVI) | R23.1 , U4.8 EVI_8 |
| Net-(U4-SCL) | R25.2 , U4.3 SCL_3 |
| Net-(U4-VBACKUP) | C10.1 , R22.1 , U4.6 VBACKUP_6 |
| OUT_POS | RShunt.2 , U3.8 Vbus_8, U3.9 Vin-_9 |
| PD_5V | C4.1 , R5.1 , R6.1 , TP4.1 1_1, U1.20 V5V_20 |
| PD_I2C_SCL_3V3 | Q1.2 S_2, TP6.1 1_1, U2.16 GPIO18_16, U3.5 SCL_5 |
| PD_I2C_SCL_5V | Q1.3 D_3, U1.5 SCL_5 |
| PD_I2C_SDA_3V3 | Q2.2 S_2, TP7.1 1_1, U2.17 GPIO19_17, U3.4 SDA_4 |
| PD_I2C_SDA_5V | Q2.3 D_3, U1.4 SDA_4 |
| PD_INT_3V3 | R8.2 , R9.1 , TP8.1 1_1, U2.18 GPIO20_18 |
| PD_INT_5V | U1.9 INT_9 |
| PD_VBUS_SENSED | C3.1 , Q4.3 D_3, R11.2 , TP2.1 1_1, U1.24 VCC_24 |
| PD_VOUT | C8.1 , Q3.3 D_3, R13.2 , RShunt.1 , TP3.1 1_1, U3.10 Vin+_10 |
| TFT_BL_PWM | R28.1 , U2.9 GPIO1/ADC1_CH1/XTAL_32K_N_9 |
| TFT_CS | J3.10 Pin_10_10, U2.11 GPIO10_11 |
| TFT_DC | J3.12 Pin_12_12, U2.12 GPIO11_12 |
| TFT_MOSI | J3.9 Pin_9_9, U2.5 MTDI/GPIO5/ADC1_CH5_5 |
| TFT_RST | J3.30 Pin_30_30, U2.23 GPIO15_23 |
| TFT_SCLK | J3.11 Pin_11_11, U2.4 MTMS/GPIO4/ADC1_CH4_4 |
| TYPE-C KONNEKTÖRÜ | J1.A4 VBUS_A4, J1.A9 VBUS_A9, J1.B4 VBUS_B4, J1.B9 VBUS_B9, TP1.1 1_1, U1.1 ISENP_1 |
| USB_CC1 | J1.A5 CC1_A5 |
| USB_CC2 | J1.B5 CC2_B5 |
| USB_DM | J1.A7 D-_A7, J1.B7 D-_B7, R3.2  |
| USB_DP | J1.A6 D+_A6, J1.B6 D+_B6, R2.2  |
| unconnected-(J1-RX1+-PadB11) | J1.B11 RX1+_B11 |
| unconnected-(J1-RX1--PadB10) | J1.B10 RX1-_B10 |
| unconnected-(J1-RX2+-PadA11) | J1.A11 RX2+_A11 |
| unconnected-(J1-RX2--PadA10) | J1.A10 RX2-_A10 |
| unconnected-(J1-SBU1-PadA8) | J1.A8 SBU1_A8 |
| unconnected-(J1-SBU2-PadB8) | J1.B8 SBU2_B8 |
| unconnected-(J1-TX1+-PadA2) | J1.A2 TX1+_A2 |
| unconnected-(J1-TX1--PadA3) | J1.A3 TX1-_A3 |
| unconnected-(J1-TX2+-PadB2) | J1.B2 TX2+_B2 |
| unconnected-(J1-TX2--PadB3) | J1.B3 TX2-_B3 |
| unconnected-(J3-Pin_2-Pad2) | J3.2 Pin_2_2 |
| unconnected-(J3-Pin_3-Pad3) | J3.3 Pin_3_3 |
| unconnected-(J3-Pin_4-Pad4) | J3.4 Pin_4_4 |
| unconnected-(J3-Pin_5-Pad5) | J3.5 Pin_5_5 |
| unconnected-(J3-Pin_6-Pad6) | J3.6 Pin_6_6 |
| unconnected-(J3-Pin_13-Pad13) | J3.13 Pin_13_13 |
| unconnected-(J3-Pin_14-Pad14) | J3.14 Pin_14_14 |
| unconnected-(J3-Pin_15-Pad15) | J3.15 Pin_15_15 |
| unconnected-(J3-Pin_16-Pad16) | J3.16 Pin_16_16 |
| unconnected-(J3-Pin_17-Pad17) | J3.17 Pin_17_17 |
| unconnected-(J3-Pin_18-Pad18) | J3.18 Pin_18_18 |
| unconnected-(J3-Pin_19-Pad19) | J3.19 Pin_19_19 |
| unconnected-(J3-Pin_20-Pad20) | J3.20 Pin_20_20 |
| unconnected-(J3-Pin_21-Pad21) | J3.21 Pin_21_21 |
| unconnected-(J3-Pin_22-Pad22) | J3.22 Pin_22_22 |
| unconnected-(J3-Pin_23-Pad23) | J3.23 Pin_23_23 |
| unconnected-(J3-Pin_24-Pad24) | J3.24 Pin_24_24 |
| unconnected-(J3-Pin_25-Pad25) | J3.25 Pin_25_25 |
| unconnected-(J3-Pin_26-Pad26) | J3.26 Pin_26_26 |
| unconnected-(J3-Pin_27-Pad27) | J3.27 Pin_27_27 |
| unconnected-(J3-Pin_28-Pad28) | J3.28 Pin_28_28 |
| unconnected-(J3-Pin_29-Pad29) | J3.29 Pin_29_29 |
| unconnected-(J3-Pin_40-Pad40) | J3.40 Pin_40_40 |
| unconnected-(Q6-D-Pad3) | Q6.3 D_3 |
| unconnected-(R4-Pad1) | R4.1  |
| unconnected-(R5-Pad2) | R5.2  |
| unconnected-(R6-Pad2) | R6.2  |
| unconnected-(R7-Pad2) | R7.2  |
| unconnected-(R8-Pad1) | R8.1  |
| unconnected-(R11-Pad1) | R11.1  |
| unconnected-(U1-CC1-Pad17) | U1.17 CC1_17 |
| unconnected-(U1-CC2-Pad16) | U1.16 CC2_16 |
| unconnected-(U1-DN-Pad18) | U1.18 DN_18 |
| unconnected-(U1-DP-Pad19) | U1.19 DP_19 |
| unconnected-(U1-FLIP-Pad6) | U1.6 FLIP_6 |
| unconnected-(U1-GPIO-Pad7) | U1.7 GPIO_7 |
| unconnected-(U1-NC-Pad2) | U1.2 NC_2 |
| unconnected-(U1-NC-Pad10) | U1.10 NC_10 |
| unconnected-(U1-NC-Pad14) | U1.14 NC_14 |
| unconnected-(U1-NC-Pad21) | U1.21 NC_21 |
| unconnected-(U2-NC-Pad22) | U2.22 NC_22 |
| unconnected-(U4-CLKOUT-Pad1) | U4.1 CLKOUT_1 |
| unconnected-(U5-BST-Pad2) | U5.2 BST_2 |
| unconnected-(U5-COMP-Pad5) | U5.5 COMP_5 |
| unconnected-(U5-EN-Pad8) | U5.8 EN_8 |
| unconnected-(U5-FB-Pad6) | U5.6 FB_6 |
| unconnected-(U5-FSW-Pad4) | U5.4 FSW_4 |
| unconnected-(U5-LX-Pad1) | U5.1 LX_1 |
| unconnected-(U5-SS-Pad7) | U5.7 SS_7 |
| unconnected-(U5-VIN-Pad9) | U5.9 VIN_9 |
