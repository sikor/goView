import segment
import entity


class Polygon(entity.Entity, entity.Parent):
    def __init__(self, points, opened=False):
        super().__init__()
        self.points = points
        self.segments = []
        self._opened = opened
        previous = None
        for point in points:
            if previous:
                lineSegment = segment.Segment(previous, point)
                lineSegment.parents.append(self)
                self.segments.append(lineSegment)
            previous = point
        if not opened and len(points) > 2:
            lineSegment = segment.Segment(previous, self.points[0])
            lineSegment.parents.append(self)
            self.segments.append(lineSegment)

    @property
    def opened(self):
        return self._opened

    def add_to_scene(self, scene):
        for lineSegment in self.segments:
            lineSegment.add_to_scene(scene)


