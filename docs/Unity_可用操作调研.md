# Unity 可用操作调研

整理一些可能由特殊输入进行控制的操作。

## 0 视角平移

移动当前视角的摄像机的位置。

view angle shift
Moves the position of the camera in the current view

考虑 x，y，z 轴方向上的平移距离。

```cs
ViewTranslate(enum Axis axis, float value)
```

## 1 视角绕自己旋转

旋转当前视角的摄像机本身。

view angle rotation
Rotate the camera itself for the current view

考虑绕 x，y，z 轴旋转的角度。

```cs
void ViewRotate(enum Axis axis, float value);
```

## 2 视角绕选中物体旋转

以选中的 GameObject 为中心，以 up 向量为轴，旋转变换当前视角的摄像机的位置，同时保持摄像机视角看向该 GameObject。

考虑旋转的角度。

Rotate the view around the selected object
Rotates the position of the camera with the selected Game Object as the center and the up vector as the axis to transform the current view, while keeping the camera view towards the Game Object.

```cs
void ViewRotateByObject(float value);
```

## 3 物体平移

移动当前选中的 GameObject。

考虑 x，y，z 轴方向上的平移距离。

Object Panning
Moves the currently selected Game Object.

```cs
void ObjectTranslate(enum Axis axis, float value);
```

## 4 物体绕自己旋转

旋转当前选中的 GameObject。

考虑绕 x，y，z 轴旋转的角度。

Object rotates around itself
Rotates the currently selected Game Object.

```cs
void ObjectRotate(enum Axis axis, float value);
```

## 5 物体缩放

缩放当前选中的 GameObject。

考虑物体沿 x，y，z 中一到三个轴的方向进行缩放。

Object Scaling
Scales the currently selected Game Object.


```cs
void ObjectScale(List<enum Axis> axis, float value);
```

## 6 实例化 Prefab

实例化一个 Prefab 并放置到当前视角正中心。

考虑 Prefab 的名称

Instantiate Prefab
Instantiates a Prefab and places it in the center of the current view.

```cs
void InitializePrefab(String name);
```